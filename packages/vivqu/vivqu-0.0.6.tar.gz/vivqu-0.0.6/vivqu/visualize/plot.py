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

from signal import raise_signal
from vivqu.quality_check.checker import QualityChecker
from vivqu.quality_check.viv_type import VivType
from vivqu.visualize.subfig import *

def pie_plot_abbrev(ax, title, detail):
    """Abbreviation for pie plot.
    """
    pie_plot(
        ax,
        detail["category"], 
        detail["data"], 
        detail["distinct"], 
        detail["completeness"], 
        title
    )


def bar_cont_abbrev(ax, title, detail):
    """Abbreviation for continuous bar plot.
    """
    bar_plot_continuous(
        ax,
        detail["labels"],
        detail["counts"],
        detail["section_div"],
        detail["completeness"],
        detail["maximum"],
        detail["median"],
        detail["minimum"],
        title
    )


def bar_disc_abbrev(ax, title, detail):
    """Abbreviation for discrete bar plot.
    """
    bar_plot_discrete(
        ax,
        detail["category"],
        detail["data"],
        detail["distinct"],
        detail["completeness"],
        detail["maximum"],
        detail["minimum"],
        title
    )


def visualize(
    checker: QualityChecker,
    df,
    column_list: list,
    date_column=None,
    max_col_per_line=3
):
    """Visualize default metrics on given columns.

    Args:
    checker: QualityChecker
        The QualityChecker object.
    df: DataFrame
        Spark or Pandas dataframe.
    column_list: list[str]
        column list to be visualized.
    date_column: str
        If specified, show date information on the graph.
    max_col_per_line: int
        Show how many columns per line.

    """
    total = len(column_list)
    # each line contains at most <max_col_per_line> sub plots
    row = (total - 1) // max_col_per_line + 1
    if total <= max_col_per_line:
        col = total
    else:
        col = max_col_per_line
    
    # each sub plot is of same size (5 * 4)
    fig, axs = plt.subplots(row, col, figsize=(4 * col, 5 * row))

    result = checker._analyze_for_visualize(df, column_list, date_column)

    idx = 0
    for instance in column_list:
        ax = (
            axs if col == 1
                else axs[idx] if row == 1
                    else axs[idx // col, idx % col]
        ) 
        detail = result[instance]
        data_type = detail["type"]
        if data_type == VivType.CATEGORY:
            pie_plot_abbrev(ax, instance, detail)
        elif data_type == VivType.CONTINUOUS:
            bar_cont_abbrev(ax, instance, detail)
        elif data_type == VivType.DISCRETE:
            bar_disc_abbrev(ax, instance, detail)
        else:
            raise Exception("Unknown data type {}".format(data_type))
        idx += 1
    
    if "_Date_" in result:
        start_date = result["_Date_"]["start"]
        end_date = result["_Date_"]["end"]
        plt.suptitle(f"{start_date} ~ {end_date}")
    
    plt.tight_layout()
    plt.show()


def visualize_corr(
        checker: QualityChecker,
        df,
        column_list,
        method="pearson"
    ):
    corr_mat = checker._corr_for_visualize(df, column_list, method)
    plt.figure(figsize=(0.6 * corr_mat.shape[1], 0.6 * corr_mat.shape[1]))
    corrplot(corr_mat)
    plt.show()


def diff(
    checker: QualityChecker,
    df_list: list,
    compare_cols: list,
    date_column=None
):
    """Differentiate two dataframes on given columns

    Agrs:
    df_list: list(DataFrame)
        Dataframes that are prepared for comparison.
    compare_cols: list(str)
        On which columns to compare.
    """
    if len(df_list) < 2:
        raise Exception("No enough dataframes to be diff!")
    if len(compare_cols) == 0:
        raise Exception("Haven't specify any column to diff!")
    
    nrows = len(compare_cols)
    ncols = len(df_list)
    fig, axs = plt.subplots(nrows, ncols, figsize=(4 * ncols, 5 * nrows))

    result_all = []
    for col in range(ncols):
        result_all.append(checker._analyze_for_visualize(df_list[col], compare_cols, date_column))

    row = 0
    for instance in compare_cols:
        ax_all = [(axs[row, col] if nrows > 1 else axs[col]) for col in range(ncols)]
        detail_all = [result_all[col][instance] for col in range(ncols)]

        instances_in_row = [instance for i in range(ncols)]

        # add date message to titles of subpots in the first row.
        if row == 0 and "_Date_" in result_all[0]:
            for col in range(ncols):
                start_date = result_all[col]["_Date_"]["start"]
                end_date = result_all[col]["_Date_"]["end"]
                instances_in_row[col] = \
                    f"{start_date} ~ {end_date}\n\n" + instances_in_row[col]

        data_type = detail_all[0]["type"]
        if data_type == VivType.CATEGORY:
            for col in range(ncols):
                pie_plot_abbrev(ax_all[col], instances_in_row[col], detail_all[col])
        elif data_type == VivType.CONTINUOUS:
            for col in range(ncols):
                bar_cont_abbrev(ax_all[col], instances_in_row[col], detail_all[col])
        elif data_type == VivType.DISCRETE:
            for col in range(ncols):
                bar_disc_abbrev(ax_all[col], instances_in_row[col], detail_all[col])
        else:
            raise Exception("Unknown data type {}".format(data_type))
        row += 1

    plt.tight_layout()
    plt.show()


# TODO: Need implementation
def trend(
    checker: QualityChecker,
    df_list: list,
    metric_list: list,
    date_column=None
):
    if len(df_list) < 2:
        raise Exception("At least two dataframes are needed.")
    if len(metric_list) == 0:
        raise Exception("At least one metrics are needed.")

    result_all = []
    for df in df_list:
        result_all.append(checker._analyze_for_trend(df, metric_list, date_column))