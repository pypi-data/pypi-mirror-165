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

from enum import Enum
from pyspark.sql import DataFrame as sparkDataFrame
from pyspark.sql.types import *


class VivType(Enum):
    CATEGORY = 0
    DISCRETE = 1
    CONTINUOUS = 2


def get_column_type_map(
    df: sparkDataFrame,
) -> dict:
    """Get the map of {column name -> data type}
    """
    column_type_map = {}
    for field in df.schema:
        column_type_map[field.name] = field.dataType
    return column_type_map


def infer_datatype(column_type_map, column):
    if column in column_type_map:
        data_type = type(column_type_map[column])
    else:
        raise Exception(f"column name {column} not exist.")

    if data_type == StringType:
        return VivType.CATEGORY
    elif data_type == IntegerType:
        return VivType.DISCRETE
    elif data_type == DoubleType:
        return VivType.CONTINUOUS
    else:
        raise Exception(f"Data type: {data_type} unable to visualize.")