import numpy as np
from typing import List, Dict
from box import Box
from pyspark.sql import DataFrame
from pyspark.sql import Column
from pyspark.sql import functions as f


class IntegralBinsGenerator:
    def generate(self, df: DataFrame, bin_params: Box) -> DataFrame:
        columns = [column for column, dtype in df.dtypes if dtype in ("tinyint", "smallint", "int", "bigint")]
        low_quantiles = self.__get_low_quantiles(df, columns, bin_params.lower_percentile_percentage, bin_params.accuracy)
        high_quantiles = self.__get_high_quantiles(df, columns, bin_params.higher_percentile_percentage, bin_params.accuracy, low_quantiles)

        return (
            df.select(*(self.__get_distinct_bins(col).alias(col) for col in columns))
            .select(
                *(
                    self.__remove_quantiles_if_bin_count_exceeds_threshold(
                        col, bin_params.bin_count, low_quantiles[col], high_quantiles[col]
                    ).alias(col)
                    for col in columns
                )
            )
            .select(
                *(
                    self.__generate_linear_bins_if_bin_count_exceeds_threshold(
                        col, bin_params.bin_count, low_quantiles[col], high_quantiles[col]
                    ).alias(col)
                    for col in columns
                )
            )
            .select(*(f.concat_ws("-", col).alias(col) for col in columns))
        )

    def __get_distinct_bins(self, col: str) -> Column:
        return f.collect_set(col)

    def __remove_quantiles_if_bin_count_exceeds_threshold(self, col: str, bin_count: int, low_quantile: int, high_quantile: int) -> Column:
        return f.when(f.size(col) <= bin_count, f.col(col)).otherwise(
            f.filter(f.col(col), lambda x: x.between(low_quantile, high_quantile))
        )

    def __generate_linear_bins_if_bin_count_exceeds_threshold(
        self, col: str, bin_count: int, low_quantile: int, high_quantile: int
    ) -> Column:
        linear_bins = (
            sorted(np.round(np.linspace(low_quantile, high_quantile, bin_count)))
            if not any([low_quantile is None, high_quantile is None])
            else []
        )

        return f.when(f.size(col) <= bin_count, f.array_sort(f.col(col))).otherwise(f.array(*map(f.lit, linear_bins)))

    def __get_low_quantiles(self, df: DataFrame, columns: List[str], lower_percentile_percentage: float, accuracy: int) -> Dict:
        low_quantiles = (
            df.select(*[f.percentile_approx(f.col(col), lower_percentile_percentage, accuracy).alias(col) for col in columns])
            .collect()[0]
            .asDict()
        )

        return low_quantiles

    def __get_high_quantiles(
        self, df: DataFrame, columns: List[str], higher_percentile_percentage: float, accuracy: int, low_quantiles: Dict
    ) -> Dict:
        high_quantiles = (
            df.select(
                *[
                    (
                        f.percentile_approx(f.when(f.col(col) > low_quantiles[col], f.col(col)), higher_percentile_percentage, accuracy) + 1
                    ).alias(col)
                    for col in columns
                ]
            )
            .collect()[0]
            .asDict()
        )

        return high_quantiles
