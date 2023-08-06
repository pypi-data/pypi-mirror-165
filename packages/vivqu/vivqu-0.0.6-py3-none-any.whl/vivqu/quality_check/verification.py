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

import re
import copy
from typing import List, Tuple, Union

import pandas as pd
from vivqu.quality_check.checker import *
from pydeequ.analyzers import *


class Verifier:
    def __init__(self, checker: QualityChecker):
        self.checker = checker


    def verify(self, df, constraint_list: List[Tuple]):
        """Verify constraints on given dataframe.
        Args:
        df: Dataframe
            The dataframe to vrify constraints on.
        constraint_list: list
            A list of constraints.
            each consists of (metric, lambda_expr, discription),
            For example: (Uniqueness("ID"), lambda x: x == 1, "No duplicate ID")

        Returns:
        result: list
            A list of boolean value. True->Success, False->Failed.
        """
        result = []
        for constraint in constraint_list:
            analyze_obj, expr, _description = constraint
            single_res = self.checker.analyze(df, [analyze_obj])
            value = single_res.iloc[0]["value"]
            succ = expr(value)
            result.append(succ)
        return result
    

    # FIXME: This method has bug, when a integet type column has str type error values,
    # the erroneous rows will be dropped, but other values in this column will remain 
    # str type, and cause exception when converting to spark dataframe.
    def check_type(
            self, 
            df, 
            col_type_list: List[Tuple[str, Union[type, str]]],
            primary_key: str
        ):
        """Check if given columns have corresponding types

        Args:
        df: DataFrame
            Spark or Pandas dataframe are all accepted.
        col_type_list: List[Tuple[str, Union[type, str]]]
            List consists of tuples of column name and expected type or regex expression. 
            If the second element is a type, check if all values in the column can be converted
            to that type; Otherwise, check if all values in the column match the regex pattern.
            For example, [("ID", str), ("amount", float), 
                ("count", int), ("date", "^[0-9]{4}-[0-9]{2}-[0-9]{2}")]
        primary_key: str
            Primary key is needed to store error values as a dict,
            The dict's key will be values in primary_key column.
        
        Returns:
        new_df: pd.DataFrame
            The new dataframe that has dropped erroneous rows.
        error_df: pd.DataFrame
            Erroreous rows that have been dropped.
        error_dict: Dict
            { primary_key -> {column, value, expected_dtype / expected_pattern} }
        """
        error_idx_list = []
        error_dict = {}

        # convert spark to pandas dataframe to use same checking procedure
        if type(df) == sparkDataFrame:
            new_df: pd.DataFrame = df.toPandas()
        else:
            new_df: pd.DataFrame = copy.deepcopy(df)
        
        # convert NaN values in pandas dataframe to None
        # thus it can be recognized by pyspark
        # new_df = new_df.replace({np.nan: None})

        for (col, dtype) in col_type_list:
            for idx, val in enumerate(new_df[col]):
                # None can be converted to any type in pyspark
                # so just ignore it.
                if pd.isnull(val):
                    continue
                # if dtype is a type, try to convert val to specific dtype
                if type(dtype) == type:
                    try:
                        val = dtype(val)
                    except:
                        error_idx_list.append(idx)
                        pm_key = new_df[primary_key][idx]
                        if pm_key not in error_dict:
                            error_dict[pm_key] = []
                        error_dict[pm_key].append({
                            "column": col,
                            "value": val,
                            "expected_dtype": str(dtype).split("'")[1]
                        })
                # if dtype is a regex expression, check if val matches it
                else:
                    regex_pattern = dtype
                    res = re.search(regex_pattern, str(val))
                    # if match failed
                    if not res:
                        error_idx_list.append(idx)
                        pm_key = new_df[primary_key][idx]
                        if pm_key not in error_dict:
                            error_dict[pm_key] = []
                        error_dict[pm_key].append({
                            "column": col,
                            "value": val,
                            "expected_pattern": regex_pattern
                        })

        # remove dupilcate element and sort it
        error_idx_list = sorted(list(set(error_idx_list)))
        # construct defective dataframe
        error_df = new_df.loc[error_idx_list, :]
        # insert index in original dataframe as a column to the left
        # error_df.insert(loc=0, column="Original_DataFrame_Index", value=error_idx_list)
        # drop erroneous rows to form a new_df
        new_df: pd.DataFrame = new_df.drop(error_idx_list)

        # create convert_dict in order to cast all cols in new_df to specified dtypes
        # convert_dict = {}
        # for (col, dtype) in col_type_list:
        #     if dtype == float:
        #         convert_dict[col] = "float64"
        # new_df = new_df.astype(convert_dict)

        # new_df.to_csv("./_tmp_.csv")
        # new_df = pd.read_csv("./_tmp_.csv")

        return new_df, error_df, error_dict