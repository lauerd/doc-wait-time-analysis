"""
SUMMARY:

This script executes the analytical workflow for this project. The broad
goal of the project is to determine if the AI algorithms that are
developed by Aidoc are effectively assisting radiologists in prioritizing
which patients they should examine first. The AI algorithms automatically
flag if a radiology patient is suspected to have a positive case of some
sort. Thus, if the algorithms are used effectively, then theoretically a
patient that is flagged as positive should have a shorter "wait time"
(i.e., the time between the aquisition of the patient's scan and the time
it is opened by a radiologist for reporting purposes).

The script produces visualizations and performs statistical analyses to
determine how "wait time" varies between AI-suspected positive and negative
patient cases. It stratifies the analysis across a variety of relevant
categorical variables.

The dataset to perform the analysis contains information about patients over
the past 6 months, since Aidoc's AI solution first went live at a customer
called "HealthyVibes" (the provider of the dataset).

TODO:

The script is currently designed to be run from the command line without
any command line arguments. If command line arguments are desired,
including an argument that specifies the script's configuration file,
then that can be set up using the "argparse" module (see the following:
https://docs.python.org/3/library/argparse.html).
"""

# Import the libraries that will be used in this script.
import pandas as pd
import numpy as np
import functions as fn
from class_to_read_config import ReadRadiologyConfig

# Interpret the configuration file that is associated with this script.
# Keep the interpreter's name small ("cfg"), as it is frequently used.
cfg = ReadRadiologyConfig()
cfg.read_config()

# Read the radiology data file in as a Pandas DataFrame.
radiology_data = pd.read_csv(cfg.get_path(cfg.PATH_DATA))

# Display the first few rows of the DataFrame.
print(radiology_data.head())

# Display the name and data type of each column in the DataFrame.
print(radiology_data.dtypes)

# Display how many rows and columns the DataFrame has.
print(radiology_data.shape)

# Display how many rows in the DataFrame are duplicated, if any.
print(radiology_data.duplicated().sum())

# Display how many missing values exist in each DataFrame column.
print(radiology_data.isna().sum())

# Remove the few DataFrame rows that contain missing values. Their
# removal is warranted, as they constitute <0.3% of all rows, and
# they are missing values from essential columns.
radiology_data.dropna(inplace=True)

# For each numeric DataFrame column of interest, plot a histogram of
# its values to view its distribution.
column_names_num = cfg.get_column_name(cfg.TIME_WAIT)
fn.plot_hist(radiology_data[column_names_num].to_frame())

# Transform skewed numeric DataFrame columns using the inverse
# hyperbolic sine transformation. Verify that the transformations
# made the columns' distributions normal by plotting histograms.
column_names_trans = f'{column_names_num}_{cfg.get_misc(cfg.TRANS)}'
radiology_data[column_names_trans] = (
    np.arcsinh(radiology_data[column_names_num])
)
fn.plot_hist(
    radiology_data[column_names_trans].to_frame(),
    x_label_nice=(
        f'{cfg.get_plot_param(cfg.LABEL)} - {cfg.get_misc(cfg.TRANS).title()}'
    )
)

# Remove the "seconds" component of the case-open DataFrame column.
# This makes the column more consistent with its study-acquisition
# counterpart column, which does not contain seconds.
(
    radiology_data[cfg.get_column_name(cfg.TIME_CO)]
    .replace(
        {cfg.get_misc(cfg.SECONDS): ''},
        regex=True,
        inplace=True
    )
)

# Convert the datetime columns in the DataFrame to the datetime type.
# Then, derive categorical columns of interest from the datetime columns
# that pertain to different scales of time (e.g., day, month, etc.).
column_names_dt = ([
    cfg.get_column_name(cfg.TIME_SA),
    cfg.get_column_name(cfg.TIME_CO)
])
formats_dt = [cfg.get_misc(cfg.DT_SA), cfg.get_misc(cfg.DT_CO)]

for counter, col in enumerate(column_names_dt):
    radiology_data = fn.add_dt_to_df(radiology_data, col, formats_dt[counter])

# Convert the boolean DataFrame column of interest into a more
# interpretable categorical column.
column_names_bool = cfg.get_column_name(cfg.RESULT)

(
    radiology_data[column_names_bool]
    .replace({
        True: cfg.get_misc(cfg.POS),
        False: cfg.get_misc(cfg.NEG)
    }, inplace=True)
)

# Re-display the first few rows of the DataFrame, now that manipulations
# and column additions have been done.
print(radiology_data.head())

# For each categorical DataFrame column, plot a bar plot of how many
# rows are in each of its categories.
column_names_cat = (
    radiology_data
    .select_dtypes(include=cfg.get_misc(cfg.CAT))
    .columns
)

radiology_data[column_names_cat].apply(fn.plot_bar)

# Plot boxplots that show how the numeric DataFrame columns of
# interest vary across the categories of other columns.
column_names_boxplot = list(map(lambda x: [x], column_names_cat))

column_names_boxplot = fn.add_list_item(
    column_names_boxplot,
    [column_names_trans, cfg.get_column_name(cfg.RESULT)]
)

list(map(lambda x: fn.plot_box(radiology_data[x]), column_names_boxplot))

# Display relevant summary statistics across the DataFrame (change the
# column names mentioned here as needed).
print(radiology_data[cfg.get_column_name(cfg.TIME_WAIT)].describe())

print(
    radiology_data
    .groupby(cfg.get_column_name(cfg.RESULT))
    [cfg.get_column_name(cfg.TIME_WAIT)]
    .describe()
)

# Display relevant statistical significance tests across the DataFrame
# (change the column names mentioned here as needed).
print(
    fn.perform_twosample_welch_ttest(
        radiology_data, cfg.get_column_name(cfg.RESULT), column_names_trans
    )
)
