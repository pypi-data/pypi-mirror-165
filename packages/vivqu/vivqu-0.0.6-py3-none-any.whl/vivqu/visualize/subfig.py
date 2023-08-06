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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.axes import Axes
from heatmap import corrplot
import seaborn as sns
sns.set(color_codes=True)

def pie_plot(
    ax: Axes, 
    category: list, 
    data: list, 
    distinct: int, 
    completeness: int, 
    title: str
):
    """Plot pie chart with given parameters.
    Args:
    ax: Axes
        Where to plot this sub figure.
    category: list
        Categories to be displayed.
    data: list
        Datas to be displayed.
    distinct: int
        Distinct values contained in this dataset.
    completeness: float
        Completeness of this dataset.
    title: str
        Title of this plot.
    """
    # if not copied in this way, the initial category and data list will
    # be change by the follwing pop operation
    raw_category = category.copy()
    raw_data = data.copy()
    data_sum = sum(raw_data)

    # calculate the completness
    if 'NullValue' in raw_category:
        null_index = raw_category.index("NullValue")
        null_cnt = raw_data[null_index]
        raw_category.pop(null_index)
        raw_data.pop(null_index)
        null_exist = True
    else:
        null_cnt = 0
        null_exist = False

    # only show first 5 categories at most    
    aggreg_cnt = 4 if null_exist else 5
    
    raw_category = np.array(raw_category)
    raw_data = np.array(raw_data)
    # get sorted indice and reverse it to sort from large to small
    indice = np.argsort(raw_data, kind="stable")
    indice = np.flipud(indice)
    # sort data and category simultaneously
    sorted_data = raw_data[indice]
    sorted_category = raw_category[indice]

    # only reserve first 5 categories (include NullValue)
    if len(sorted_category) > aggreg_cnt:
        curr_sum = sorted_data[: aggreg_cnt - 1].sum()
        sorted_category = np.append(sorted_category[: aggreg_cnt - 1], "OtherValues")
        sorted_data = np.append(sorted_data[: aggreg_cnt - 1], data_sum - null_cnt - curr_sum)
    if null_exist:
        sorted_category = np.append("NullValue", sorted_category)
        sorted_data = np.append(null_cnt, sorted_data)

    # cut texts that are too long to display in the canvas
    show_category = []
    for idx in range(len(sorted_category)):
        curr_str = sorted_category[idx]
        if len(curr_str) > 20:
            curr_str = curr_str[:20] + "..."
        show_category.append(curr_str)
    
    # ensure that only NullValue is showed in red color (C3)
    if null_exist:
        color_palatte = ['C3', 'C0', 'C1', 'C2', 'C4', 'C5']
    else:
        color_palatte = ['C0', 'C1', 'C2', 'C4', 'C5', 'C6']
    
    ax.pie(
        sorted_data, 
        labels=show_category, 
        colors=color_palatte,
        labeldistance=None, 
        pctdistance=1.2, 
        autopct='%.1f%%', 
        frame=1
    )

    # draw the central grey circle
    # this color is the same as background color
    ax.pie([1], radius=0.7, colors=['0.918'], frame=1)

    ax.text(
        0, 1.4,
        'Completness: {:.4f}\n'
        'Distinct values: {:d}'
        .format(completeness, distinct),
        horizontalalignment="center", 
        verticalalignment="bottom",
    )
    
    ax.legend(loc='upper center')
    # put pins to stretch out the canvas
    # can not use set_ylim because ax.axis('euqal') will interfere with it
    ax.scatter([0, 0], [3.6, -1.2], marker='.', color='white', alpha=0)

    # ensure equal scale of pie chart by changing axis limits
    # Important: without this, it can not both fullfill the box and make circle circular
    # Reference: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axis.html
    ax.axis('equal') 
    ax.set_xlim((-1.7, 1.7))
    # pie chart do not need axis scale
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title(title)


def bar_plot_continuous(
    ax: Axes,
    labels: list,
    counts: list,
    section_div: list,
    completeness: float, 
    max_val: float, 
    med_val: float, 
    min_val: float,
    title: str
):
    """Plot continuous bar chart

    To adapt to the bias of data distribution, the bar plot function
    divides `counts` array into three sections, as `section_div` indicates,
    the extremely small or large but alse extremely sparse parts are 
    `section_div[0]` and `section_div[2]`, which is shown as orange and red bars,
    the normal part is `section_div[1]`, which is shown as blue bars.

    Args:
    labels: list
        labels shown at the xtick.
    counts: list
        count of each bar.
    section_div: list
        section_div[0] indicates count of small but sparse part, 
        section_div[1] indicates count of normal part,
        section_div[2] indicates count of large but sparse part.
        sum(section_div) should equal len(counts).
    completeness:
        Completeness of this dataframe.
    max_val, med_val, min_val: float
        maximum, median, mininum values.
    title: str
        Title of this chart.
    """
    [left_count, main_count, right_count] = section_div
    
    ticks = [i for i in range(len(labels))]
    labels = [format(i, ".1f") for i in labels]

    ax.set_xticks(ticks, labels, rotation=30)

    for i in range(left_count):
        ax.get_xticklabels()[i].set_color("tab:orange")
    for i in range(right_count):
        ax.get_xticklabels()[-i-1].set_color("tab:red")

    for idx in range(left_count):
        # plot the box
        ax.add_patch(
            patches.Rectangle(
                (ticks[idx] + 0.1, 0),
                0.8,
                counts[idx],
                color="tab:orange"
            )
        )
    for idx in range(main_count):
        # plot the box
        ax.add_patch(
            patches.Rectangle(
                (ticks[idx + left_count] + 0.1, 0),
                0.8,
                counts[idx + left_count],
                color="tab:blue"
            )
        )
    for idx in range(right_count):
        # plot the box
        ax.add_patch(
            patches.Rectangle(
                (ticks[idx + left_count + main_count] + 0.1, 0),
                0.8,
                counts[idx + left_count + main_count],
                color="tab:red"
            )
        )

    height = np.max(counts) * 1.1
    width = len(counts) + 0.5

    for idx in range(len(counts)):
        place_x = idx + 0.5
        place_y = counts[idx] + height / 50
        ax.text(
            place_x, place_y, 
            str(counts[idx]), 
            horizontalalignment="center", 
            verticalalignment="center"
        )

    ax.text(
        0.96, 0.96, 
        "Completeness: {:.4f}\n\n"
        "Maximum: {:.2f}\n"
        "Median:    {:.2f}\n"
        "Minimum:  {:.2f}"
        .format(completeness, max_val, med_val, min_val),
        horizontalalignment="right", 
        verticalalignment="top",
        multialignment="left",
        transform = ax.transAxes
    )

    ax.set_xlim((-0.5, width))
    ax.set_ylim((0, height))
    ax.set_title(title)


def bar_plot_discrete(
    ax: Axes,
    category: list, 
    data: list, 
    distinct: int,
    completeness: float,
    max_val: float, 
    min_val: float,
    title: str
):
    """Plot discrete bar chart

    Args:
    category: list
        Categories to be displayed.
    data: list
        Datas to be displayed.
    distinct: int
        Distinct values contained in this dataset.
    completeness: float
        Completeness of this dataset.
    max_val, min_val: float
        maximum, mininum values.
    title: str
        Title of this chart.
    """
    ax.bar(category, data, edgecolor="tab:blue")
    ax.text(
        0.96, 0.96, 
        "Completeness: {:.4f}\n"
        "Distinct Values: {:d}\n\n"
        "Maximum: {:.2f}\n"
        "Minimum: {:.2f}"
        .format(completeness, distinct, max_val, min_val),
        horizontalalignment="right", 
        verticalalignment="top",
        multialignment="left",
        transform = ax.transAxes
    )
    ax.set_title(title)


# DEPRECATED
def box_plot(
    ax: Axes, 
    Q1: float, 
    Q2: float, 
    Q3: float, 
    min_val: float, 
    max_val: float, 
    completness: float, 
    title: str
):
    """plot box figure
    Args:
    ax: Axes
        Where to plot this sub figure.
    Q1, Q2, Q3: float
        The 0.25, 0.5, 0.75 quantiles.
    min_val, max_val: float
        Minimum and maxinum value.
    completeness: float
        Completeness to be displayed.
    title: str
        Title to be displayed.
    """
    # several metrics needed for drawing
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR

    # plot the box
    ax.add_patch(
        patches.Rectangle(
            (-0.6, Q1),
            1.2,
            IQR,
            edgecolor='black',
            fill=False
        ))

    # vertival line
    ax.plot([0, 0], [lower_whisker, Q1], color='black', linewidth=1)
    ax.plot([0, 0], [Q3, upper_whisker], color='black', linewidth=1)
    # median value
    ax.plot([-0.6, 0.6], [Q2, Q2], color='orange', linewidth=1)
    # lower and upper whisker
    ax.plot([-0.3, 0.3], [lower_whisker, lower_whisker], color='black', linewidth=1)
    ax.plot([-0.3, 0.3], [upper_whisker, upper_whisker], color='black', linewidth=1)
    # minimum and maximum value
    ax.scatter([0, 0], [min_val, max_val], color='b', facecolors='none')

    # where to place the texts
    highest = max(max_val, upper_whisker)
    lowest = min(min_val, lower_whisker)
    text_place = (2 * highest + 3 * lowest) / 5

    ax.text(
        1.2, text_place, 
        'Completeness: {:.2f}\n\n'
        'Max:      {:.2f}\n\n'
        'Q-75%:  {:.2f}\n'
        'Q-50%:  {:.2f}\n'
        'Q-25%:  {:.2f}\n\n'
        'Min:      {:.2f}\n'
        .format(completness, max_val, Q3, Q2, Q1, min_val)
    )
        
    ax.get_xaxis().set_visible(False)
    ax.set_xlim((-1.7, 5.1))
    ax.set_title(title)