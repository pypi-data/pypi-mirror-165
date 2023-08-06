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

from pydeequ.analyzers import *
from pydeequ.profiles import *
from pydeequ.checks import *
from pydeequ.verification import *
from vivqu.quality_check.viv_type import *

class DeequAnalysisBuilder:
    """Analyze runner builder

    The class provides a builder to add various analyzers and settings
    and finally run them. This is actually an encapsulation over 
    pydeequ's AnalysisRunBuilder.

    In most cases, this class will not be accessed by users, as its functions
    are wrapped by QualityChecker.analyze().

    Example:
    >>> analyer = AnalyzeBuilder(spark_session, df)         # initialize the builder
    >>> analyzer.add_default("amount")                      # use default analysis setting
    >>> analyzer.add(Sum("amount")).add(Histogram("cost"))  # add some other metrics
    >>> result_df = analyzer.run()                          # run it and get the result

    Args:
    spark: SparkSession
        The spark session used to analyzing data.
    dataframe: DataFrame
        The data frame object that need analysis.
    """
    def __init__(self, spark_session: SparkSession, df: DataFrame):
        self._spark_session = spark_session
        self._df = df
        self._AnaysisRunBuilder = AnalysisRunBuilder(spark_session, df)
    

    def add(self, analyzer_obj):
        """Add new analyzer to the builder

        Args:
        analyzer: _AnalyzerObject
            An analyer object derived from basic class _AnalyzerObject,
            including Completness(), Mean(), Size(), Sum() and so on.
        
        Returns:
        self: AnalyzeBuilder
            For further chained method calls.
        """
        self._AnaysisRunBuilder.addAnalyzer(analyzer_obj)
        return self


    def add_default(self, column, data_type):
        """Add default analyzers to the given column

        Provide Completness, CountDistinct and Histogram metrics for text type,
        provide Completness, ApproxQuantiles, Maximum, Minimum metrics for numeric type,

        Args:
        column: str
            Add default metrics to which column.
        data_type: UpperType
            One type of [CATEGORY, DISCRETE, CONTINUOUS]

        Returns:
        self: AnalyzeBuilder
            For further chained method calls.
        """

        self._AnaysisRunBuilder.addAnalyzer(Completeness(column))
        # if this field is text type
        if data_type == VivType.CATEGORY:
            self._AnaysisRunBuilder.addAnalyzer(CountDistinct([column]))
            self._AnaysisRunBuilder.addAnalyzer(Histogram(column))
        # if this field is numeric type
        elif data_type == VivType.CONTINUOUS :
            self._AnaysisRunBuilder.addAnalyzer(ApproxQuantiles(column, quantiles=[0.25, 0.5, 0.75]))
            self._AnaysisRunBuilder.addAnalyzer(Maximum(column))
            self._AnaysisRunBuilder.addAnalyzer(Minimum(column))
            self._AnaysisRunBuilder.addAnalyzer(Mean(column))
        elif data_type == VivType.DISCRETE:
            self._AnaysisRunBuilder.addAnalyzer(CountDistinct([column]))
            self._AnaysisRunBuilder.addAnalyzer(Histogram(column))
            self._AnaysisRunBuilder.addAnalyzer(Maximum(column))
            self._AnaysisRunBuilder.addAnalyzer(Minimum(column))
        else:
            raise Exception(f"Unknown data type: {data_type}")

        return self
    
    
    def run(self):
        """Run the analyze builder

        The above methods only add settings to the builder, this method actually
        runs analyzing and saves the result.

        Returns:
        analysis_result_df: DataFrame
            Analysis result as the DataFrame object.
        """
        analysis_result = self._AnaysisRunBuilder.run()
        analysis_result_df = AnalyzerContext.successMetricsAsDataFrame(self._spark_session, analysis_result)

        return analysis_result_df
