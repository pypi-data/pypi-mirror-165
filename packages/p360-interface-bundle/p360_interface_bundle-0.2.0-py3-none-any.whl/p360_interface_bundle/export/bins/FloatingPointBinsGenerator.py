from box import Box
from pyspark.sql import DataFrame
from pyspark.sql import Column
from pyspark.sql import functions as f


class FloatingPointBinsGenerator:
    def generate(self, df: DataFrame, bin_params: Box) -> DataFrame:
        columns = [column for column, dtype in df.dtypes if dtype in ("float", "double")]

        return df.select(
            *(
                self.__count_percentile(col, bin_params.higher_percentile_percentage, bin_params.accuracy).alias(f"{col}_quantile")
                for col in columns
            ),
            *(f.max(col).alias(f"{col}_max") for col in columns),
        ).select(*(self.__make_bin_string(col, bin_params.bin_count).alias(col) for col in columns))

    def __count_percentile(self, col: str, percentile_percentage: float, accuracy: int) -> Column:
        return f.percentile_approx(f.when(f.col(col) > 0, f.col(col)), percentile_percentage, accuracy)

    def __round_bin(self, col: str, current_bin: int, bin_count: int) -> Column:
        return current_bin * f.col(f"{col}_quantile") / (bin_count - 1)

    def __make_bin_array(self, col: str, bin_count: int) -> Column:
        return f.array_distinct(f.array(*(self.__round_bin(col, i, bin_count - 1) for i in range(bin_count - 1)), f.col(f"{col}_max")))

    def __make_bin_string(self, col: str, bin_count: int) -> Column:
        return f.concat_ws("-", self.__make_bin_array(col, bin_count))
