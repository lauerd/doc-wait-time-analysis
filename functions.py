"""
SUMMARY:

This script defines the functions that are used to support the analyses
conducted in this project's primary script: "main.py". Each function
contains a docstring that describes it in more detail.
"""

# Import the libraries that will be used in this script.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from class_to_read_config import ReadRadiologyConfig

# Interpret the configuration file that is associated with this script.
# Keep the interpreter's name small ("cfg"), as it is frequently used.
cfg = ReadRadiologyConfig()
cfg.read_config()


# Define functions that relate to processing data.
def add_dt_to_df(
        df, colname, dt_format,
        dt_mo=cfg.get_misc(cfg.MONTH),
        dt_mo_fmt=cfg.get_misc(cfg.DT_MO)):
    """Add datetime columns to a pandas DataFrame.

    First convert a relevant string/categorical column to the
    datetime data type, and then extract new columns from that column
    that describe different scales of time (e.g., month).

    Args:
        df (pandas DataFrame): DataFrame containing the columns.
        colname (string): name of the DataFrame column with datetime info.
        dt_format (string): format of the datetime info in the column.
        dt_mo (string): reference of how to refer to a month.
        dt_mo_fmt (string): format to extract month from datetime info.

    Returns:
        pandas DataFrame: DataFrame with datetime columns processed.
    """

    # Convert "colname" to the datetime type.
    df[colname] = pd.to_datetime(df[colname], format=dt_format)

    # Extract new columns that describe different scales of time.
    df[f'{colname}_{dt_mo}'] = df[colname].dt.strftime(dt_mo_fmt)

    return df


def add_list_item(list_of_lists, item):
    """Add the same item to each element of a list of lists.

    Args:
        list_of_lists (list): list of lists to add an item to.
        item ([flexible type]): the item to add.

    Returns:
        list: list of lists with the item added to each element.
    """

    return [sublist+item for sublist in list_of_lists]


# Define functions that relate to making visualizations.
def set_plot_size(
        plot_width=int(cfg.get_plot_param(cfg.WIDTH)),
        plot_height=int(cfg.get_plot_param(cfg.HEIGHT))):
    """Set the width * height dimensions of a plot.

    Args:
        plot_width (int): width of the plot.
        plot_height (int): height of the plot.

    Returns:
        tuple: paired width and height of a plot.
    """

    plot_size = (plot_width, plot_height)
    return plot_size


def set_plot_axes(
        ax, label_x, label_y=None,
        label_size=int(cfg.get_plot_param(cfg.SIZE_AXIS)),
        label_pad=int(cfg.get_plot_param(cfg.PAD)),
        tick_label_size=int(cfg.get_plot_param(cfg.SIZE_TICK)),
        tick_rotation=cfg.get_plot_param(cfg.ROTATION),
        legend_bool=cfg.get_plot_param(cfg.LEGEND) == 'True'):
    """Designate the settings and format of a plot's axes.

    Args:
        ax (axes object): the current plot axes that should be modified.
        label_x (string): x-axis label to add to the plot.
        label_y (string): y-axis label to add to the plot.
        label_size (int): size of an axis label's text.
        label_pad (int): distance between an axis label and its axis ticks.
        tick_label_size (int): size of an axis tick label's text.
        tick_rotation (string): orientation of the axes' tick labels.
        legend_bool (bool): should a plot legend be included or not?

    Returns:
        axes object: object containing a plot axes' settings and format.
    """

    # Set the text and format of the current plot's axis labels.
    ax.set_xlabel(label_x, fontsize=label_size, labelpad=label_pad)
    ax.set_ylabel(label_y, fontsize=label_size, labelpad=label_pad)

    # Set the format of the current plot's axis ticks.
    ax.tick_params(labelsize=tick_label_size)
    plt.xticks(rotation=tick_rotation)

    # Determine whether or not a plot legend should be included.
    if not legend_bool:
        ax.legend_ = None

    return ax


def plot_hist(
        plot_data,
        x_label_nice=cfg.get_plot_param(cfg.LABEL),
        plot_type=cfg.get_plot_param(cfg.HIST),
        path=cfg.get_path(cfg.PATH_PLOTS),
        plot_format=cfg.get_plot_param(cfg.FORMAT)):
    """Plot a histogram of a pandas DataFrame column with chosen settings.

    Args:
        plot_data (pandas DataFrame): DataFrame containing the column.
        x_label_nice (string): polished label for the plot's x-axis.
        plot_type (string): the type of plot being made (i.e., hist).
        path (string): the file path where the plot file will be saved.
        plot_format (string): the format of the file containing the plot.
    """

    # Designate the plot's file name.
    plot_name = f'{plot_type}_{plot_data.columns[0]}'

    # Remove any reference to previous plots, so that a new plot can be made.
    plt.clf()

    # Make the plot. Designate its size and the text and format of its axes.
    plot_out = plot_data.plot.hist(figsize=set_plot_size())
    plot_out = set_plot_axes(plot_out, x_label_nice)

    # Save the plot as a file.
    plot_out = plot_out.get_figure()
    plot_out.savefig(f'{path}{plot_name}{plot_format}')


def plot_bar(
        plot_data,
        time_keyword=cfg.get_misc(cfg.TIME),
        plot_type=cfg.get_plot_param(cfg.BAR),
        edge_color=cfg.get_plot_param(cfg.COLOR_BE),
        path=cfg.get_path(cfg.PATH_PLOTS),
        plot_format=cfg.get_plot_param(cfg.FORMAT)):
    """Plot a bar plot of a pandas DataFrame column with chosen settings.

    Args:
        plot_data (pandas DataFrame): DataFrame containing the column.
        time_keyword (string): keyword representing datetime info.
        plot_type (string): the type of plot being made (i.e., bar).
        edge_color (string): color of the edges of the plot's bars.
        path (string): the file path where the plot file will be saved.
        plot_format (string): the format of the file containing the plot.
    """

    # Determine the frequency of each category in the DataFrame column.
    plot_data = plot_data.value_counts().to_frame()

    # If the column contains datetime info, sort categories chronologically.
    if time_keyword in plot_data.index.name:
        plot_data = plot_data.sort_index()

    # Designate the text of the plot's x-axis.
    x_label = plot_data.index.name
    x_label_nice = x_label.title().replace('_', ' ')

    # Designate the plot's file name.
    plot_name = f'{plot_type}_{x_label}'

    # Remove any reference to previous plots, so that a new plot can be made.
    plt.clf()

    # Make the plot. Designate its size and the text and format of its axes.
    plot_out = (
        plot_data.plot.bar(
            figsize=set_plot_size(),
            edgecolor=edge_color
        )
    )
    plot_out = set_plot_axes(plot_out, x_label_nice)

    # Save the plot as a file.
    plot_out = plot_out.get_figure()
    plot_out.savefig(f'{path}{plot_name}{plot_format}')


def plot_box(
        plot_data,
        time_keyword=cfg.get_misc(cfg.TIME),
        plot_type=cfg.get_plot_param(cfg.BOX),
        line_width=int(cfg.get_plot_param(cfg.LWD)),
        point_color=cfg.get_plot_param(cfg.COLOR_PT),
        legend_size=int(cfg.get_plot_param(cfg.SIZE_TICK)),
        path=cfg.get_path(cfg.PATH_PLOTS),
        plot_format=cfg.get_plot_param(cfg.FORMAT)):
    """Plot a box plot of pandas DataFrame columns with chosen settings.

    Args:
        plot_data (pandas DataFrame): DataFrame containing three columns:
            1) a column of categories; 2) a numeric column; and 3) another
            column of categories to potentially distinguish boxes by color.
        time_keyword (string): keyword representing datetime info.
        plot_type (string): the type of plot being made (i.e., box).
        line_width (int): width of the lines and borders of the plot's boxes.
        point_color (string): color of the plot's points.
        legend_size (int): size of the legend's text.
        path (string): the file path where the plot file will be saved.
        plot_format (string): the format of the file containing the plot.
    """

    # Designate the text of the plot's axes.
    x_label = plot_data.columns[0]
    x_label_nice = x_label.title().replace('_', ' ')
    y_label = plot_data.columns[1]

    # Determine if a third categorical column should be included to further
    # distinguish boxes by another category using box color.
    if x_label is not plot_data.columns[2]:
        z_label = plot_data.columns[2]
    else:
        z_label = None
        plot_data = plot_data.iloc[:, :-1]

    # If a column contains datetime info, sort the DataFrame chronologically.
    if time_keyword in x_label:
        plot_data = plot_data.sort_values(x_label)

    # Designate the plot's file name.
    plot_name = f'{plot_type}_{x_label}'

    # Remove any reference to previous plots, so that a new plot can be made.
    plt.clf()

    # Make the plot. Designate the text and format of its axes and plot body.
    plot_out = sns.boxplot(
        data=plot_data,
        x=x_label,
        y=y_label,
        hue=z_label,
        linewidth=line_width,
        flierprops=dict(markerfacecolor=point_color)
    )
    plot_out = set_plot_axes(plot_out, x_label_nice)

    # Determine whether or not a legend should be included.
    if z_label is not None:
        plot_out.legend(fontsize=legend_size)

    # Save the plot as a file.
    plot_out.figure.savefig(f'{path}{plot_name}{plot_format}')


# Define a function that performs a statistical significance test.
def perform_twosample_welch_ttest(df, column_name_cat, column_name_num):
    """Perform a two-sample Welch's t-test.

    The Welch's t-test is preferred over the more traditional student's
    t-test, because it can better handle cases where the two samples of
    interest are unequal in variance and/or sample size.

    Args:
        df (pandas DataFrame): DataFrame containing the samples.
        column_name_cat (string): name of the categorical column whose
            categories distinguish which rows fall into which sample.
        column_name_num (string): name of the numeric column to test.

    Returns:
        TtestResult object: object containing the outcomes of the test.
    """

    # Determine the names of the categories that represent separate samples.
    cats = df[column_name_cat].unique()

    # Designate the two samples to test.
    test_sample_x = df.loc[df[column_name_cat] == cats[0], column_name_num]
    test_sample_y = df.loc[df[column_name_cat] == cats[1], column_name_num]

    # Perform the t-test and return the outputs. Note that "equal_var=False"
    # is what makes this a Welch's t-test specifically.
    return stats.ttest_ind(test_sample_x, test_sample_y, equal_var=False)
