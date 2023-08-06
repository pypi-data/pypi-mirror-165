from typing import List, Dict
from box import Box
from pyspark.sql import DataFrame
from pyspark.sql import functions as f


class CategoricalBinsReducer:
    def reduce(self, df: DataFrame, columns: List[str], bin_params: Box) -> DataFrame:
        columns = [column for column, dtype in df.dtypes if dtype == "string"]
        threshold = 1 - bin_params.reduction_percentage

        for col in columns:
            category_counts = self.__get_category_counts(df, col)
            number_of_categories = len(category_counts)
            total_count = sum(category_counts.values())
            percentage_count = 0
            categories_under_threshold = []

            if number_of_categories <= bin_params.minimum_categories_to_apply_reduction:
                continue

            for category, count in sorted(category_counts.items(), key=lambda item: item[1], reverse=True):
                if percentage_count < threshold:
                    categories_under_threshold.append(category)

                category_percentage = count * 100 / total_count
                percentage_count += category_percentage

            df = df.withColumn(
                col,
                f.when(f.col(col).isin(categories_under_threshold) | f.col(col).isNull(), f.col(col)).otherwise("other"),
            )

        return df

    def __get_category_counts(self, df: DataFrame, col: str) -> Dict:
        return (
            df.select(col).na.drop().groupBy(col).count().select(f.map_from_entries(f.collect_list(f.struct(col, "count")))).collect()[0][0]
        )
