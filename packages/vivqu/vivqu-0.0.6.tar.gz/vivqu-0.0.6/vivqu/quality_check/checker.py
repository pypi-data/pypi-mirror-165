# Copyright 2022 Airwallex.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
from pyspark.mllib.stat import Statistics
from pyspark.sql import DataFrame as sparkDataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from pyspark.sql.functions import countDistinct

from vivqu.quality_check.deequ_wrap import DeequAnalysisBuilder
from vivqu.quality_check.viv_type import *

from pydeequ.checks import *
from pydeequ.verification import *

class QualityChecker:
    """Data quality checker

    This class is designed for data quality checking based on different databases
    like mysql, postgresql and bigQuery. It provides functions, include metrics analyzing,
    profile messages visualizing, constraint suggestion and constraint verification.

    Example:
    >>> checker = QualityChecker(spark_session)
    >>> analysis_result = checker.analyze(
            df, ["dtime", "age", Mean("money")],
            "date_created"
        )
    >>> corr_mat_df = checker.corr(
            df, ["speed", "time", "cost"]
        )

    Args:
    spark_session: SparkSession
        The spark session used to analyzing data.
    """

    def __init__(self, spark_session: SparkSession):
        self._spark_session = spark_session
    

    def convert_to_spark(self, df):
        """Convert a Pandas Dataframe to Spark Dataframe.
        """
        if type(df) == sparkDataFrame:
            pass # it should be spark dataframe, do nothing.
        elif type(df) == pd.DataFrame:
            # IMPORTANT!
            # without this, spark will recognize np.nan in pd.DataFrame as type float,
            # and cause some weird errors.
            df = df.replace({np.nan: None})
            # if user pass pandas dataframe, convert it to spark dataframe.
            df = self._spark_session.createDataFrame(df)
        else:
            raise Exception(f"Unknown type of parameter df: {type(df)}")
        return df


    def analyze(
        self, 
        df: sparkDataFrame,
        metric_list,
        date_column=None
    ) -> pd.DataFrame:
        """Analyze metrics on the data frame.

        Example:
        >>> result = self.analyze(
                df, [
                "age",
                "country",
                Mean("money"),
                Completness("date"),
                ],
                "start_date"
            )

        Args:
        df: DataFrame
            Analyze on which dataframe.
        metric_list: List
            Analyzers to be added to the dataframe.
            If type is string, then add default metrics to the column,
            otherwise, add specified metric to the column.
        date_column: str
            Specify the column of date if needed. The start and end date will be
            appended in the analysis result, and will be shown on the picture
            by visualizer.

        Returns:
        result: pd.DataFrame
            The analysis result of default metric.
        """

        df = self.convert_to_spark(df)

        analyzer = DeequAnalysisBuilder(self._spark_session, df)

        column_type_map = get_column_type_map(df)

        for analyzer_obj in metric_list:
            # add default metrics to the column
            if type(analyzer_obj) == str:
                column = analyzer_obj
                data_type = infer_datatype(column_type_map, column)
                analyzer.add_default(column, data_type)
            # add specific metric to the column
            else:
                analyzer.add(analyzer_obj)

        result = analyzer.run().toPandas()

        if date_column != None:
            date_max, date_min = self._date_analyze(df, date_column)
            # manually add them to the result dataframe
            result.loc[len(result.index)] = ["Dataset", "*", "StartDate", date_min]
            result.loc[len(result.index)] = ["Dataset", "*", "EndDate", date_max]

        return result
    

    def corr(
        self,
        df: sparkDataFrame,
        column_list: list,
        method='pearson'
    ) -> pd.DataFrame:
        """Calculate correlation matrix of given columns.
        Args:
        df:
            Analyze on which dataframe.
        columns:
            Calculate on which columns.
        method:
            The method used to calculate correlation.
            Support 'pearson' (default), 'spearman'

        Returns:
        corr_mat_df: pd.DataFrame
            Correlation matrix of specified columns.
        """
        df = self.convert_to_spark(df)

        # select columns to calculate
        if len(column_list) > 0:
            sub_df = df.select(column_list)
        else:
            sub_df = df
        # convert dataframe to rdd
        df_rdd = sub_df.rdd.map(lambda row: row[0:])
        corr_mat = Statistics.corr(df_rdd, method=method)
        corr_mat_df = pd.DataFrame(
            corr_mat,
            columns=sub_df.columns, 
            index=sub_df.columns
        )
        return corr_mat_df

    
    def _analyze_for_trend(
        self,
        df,
        metric_list,
        date_column=None
    ):
        """This method is prepared for trend function.
        """
        result = []
        df = self.convert_to_spark(df)
        for metric in metric_list:
            value = self.analyze(df, [metric]).at[0, "value"]
            result.append(value)
        if date_column != None:
            date_max, date_min = self._date_analyze(df, date_column)
            result += [date_min, date_max]
        return result
        


    def _analyze_for_visualize(
        self,
        df,
        column_list,
        date_column=None
    ):
        """This method is prepared for visualization function.
        The result is in the format of dict, not dataframe.
        """
        df = self.convert_to_spark(df)

        result = {}
        column_type_map = get_column_type_map(df)
        for column in column_list:
            data_type = infer_datatype(column_type_map, column)
            if data_type == VivType.CATEGORY:
                result[column] = self._category_analyze(df, column)
            elif data_type == VivType.DISCRETE:
                result[column] = self._discrete_analyze(df, column)
            elif data_type == VivType.CONTINUOUS:
                result[column] = self._continuous_analyze(df, column)
            else:
                raise Exception(f"Unknown data type: {data_type}")
        
        if date_column != None:
            date_max, date_min = self._date_analyze(df, date_column)
            result["_Date_"] = {}
            result["_Date_"]["end"] = date_max
            result["_Date_"]["start"] = date_min
        
        return result


    def _category_analyze(
        self,
        df,
        column
    ):
        """Get metrics for categorical visualization.
        """
        count = df.agg({column: "count"}).collect()[0][0]
        size = df.count()
        completeness = count / size

        distinct = df.select(countDistinct(column)).collect()[0][0]
        histogram = df.groupBy(column).agg({"*": "count"}).collect()

        category = []
        data = []

        for idx in range(len(histogram)):
            name = "NullValue" if histogram[idx][0] == None else histogram[idx][0]
            value = histogram[idx][1]
            category.append(name)
            data.append(value)
        
        return {
            "type": VivType.CATEGORY,
            "category": category,
            "data": data,
            "distinct": distinct,
            "completeness": completeness
        }


    def _discrete_analyze(
        self,
        df,
        column
    ):
        """Get metrics for discrete numeric visualization.
        """
        result = self._category_analyze(df, column)
        result["type"] = VivType.DISCRETE
        result["maximum"] = df.agg({column: "max"}).collect()[0][0]
        result["minimum"] = df.agg({column: "min"}).collect()[0][0]
        return result


    def _continuous_analyze(
        self,
        df,
        column  
    ):
        """Get metrics for continuous numeric visualization.
        """
        count = df.agg({column: "count"}).collect()[0][0]
        size = df.count()
        completeness = count / size

        maximum = df.agg({column: "max"}).collect()[0][0]
        minimum = df.agg({column: "min"}).collect()[0][0]

        sql_percentile = f"percentile_approx({column}, array(0.05, 0.5, 0.95))"
        mass_begin, median, mass_end = df.agg(expr(sql_percentile)).collect()[0][0]

        # check if this column has extremely large or small data point
        end_norm = True if maximum - mass_end < 0.6 * (mass_end - mass_begin) else False
        begin_norm = True if mass_begin - minimum < 0.6 * (mass_end - mass_begin) else False

        buckets = []
        left_count = right_count = norm_count = 0

        def even_slice(begin, end, num, pop=""):
            """Get even slices for `begin` to `end` of count ``num`.
            If `pop` is set as "begin" or "end", pop the first or last element.
            """
            buckets = []
            for i in range(num + 1):
                buckets.append((i * end + (num - i) * begin) / num)
            if pop == "end":
                buckets.pop()
            elif pop == "begin":
                buckets.pop(0)
            return buckets

        # compress sparse begin or end parts, to make the figure look more reasonable
        if begin_norm and end_norm:
            norm_count = 8
            buckets = even_slice(minimum, maximum, 8)
        elif begin_norm and not end_norm:
            right_count = 3
            norm_count = 5
            buckets = even_slice(minimum, mass_end, 5) + \
                even_slice(mass_end, maximum, 3, pop="begin")
        elif not begin_norm and end_norm:
            left_count = 3
            norm_count = 5
            buckets = even_slice(minimum, mass_begin, 3, pop="end") + \
                even_slice(mass_begin, maximum, 5)
        else:
            left_count = right_count = norm_count = 3
            buckets = even_slice(minimum, mass_begin, 3, pop="end") + \
                even_slice(mass_begin, mass_end, 3) + \
                even_slice(mass_end, maximum, 3, pop="begin")
        
        labels, counts = df.select(column).rdd.flatMap(lambda x: x).histogram(buckets)

        return {
            "type": VivType.CONTINUOUS,
            "labels": labels,
            "counts": counts,
            "section_div": [left_count, norm_count, right_count],
            "maximum": maximum,
            "median": median,
            "minimum": minimum,
            "completeness": completeness
        }
    

    def _date_analyze(
        self,
        df,
        date_column
    ):
        """Get start and end date from given dataframe.
        """
        date_max = df.agg({date_column: "max"}).collect()[0][0]
        date_min = df.agg({date_column: "min"}).collect()[0][0]
        # drop detailed time information, reserve date only
        date_max = str(date_max).split(' ')[0]
        date_min = str(date_min).split(' ')[0]
        return date_max, date_min
            

    def _corr_for_visualize(
        self,
        df,
        column_list,
        method="pearson"
    ):
        """This method is prepared for visualization.
        """
        return self.corr(df, column_list, method)