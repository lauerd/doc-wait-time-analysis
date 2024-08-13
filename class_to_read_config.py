"""
SUMMARY:

This script creates a class that interprets the text that is contained
within this project's configuration file. It allows for the file to be
interpreted as needed within the project's other scripts.

The configuration file contains all parameters that are associated with
this project's analyses. By listing all parameters in the same place,
this file makes the analyses more readily reusable and modifiable by
other users.
"""

# Import the libraries that will be used in this script.
import configparser


# Define the class (see summary above).
class ReadRadiologyConfig:
    """Interpret this project's .ini configuration file.

    Returns:
        string: strings of the file's various parameters.
    """

    # List the parameters that reference the file's structure.
    FILE = 'config.ini'
    PATHS = 'file_paths'
    NAMES = 'dataset_column_names'
    PLOTS = 'output_plots'
    MISC = 'miscellaneous'

    # List the parameters that references the file's dataset.
    PATH_DATA = 'dataset'
    PATH_PLOTS = 'output_plots'

    # List the parameters that reference the dataset's column names.
    SITE = 'aidoc_site'
    ALGORITHM = 'algorithm'
    CLASS = 'patient_class'
    RESULT = 'aidoc_result'
    TIME_WAIT = 'wait_time_minutes'
    TIME_SA = 'study_aquistion_time'
    TIME_CO = 'case_open_time'

    # List the parameters that reference how plots are made.
    COLOR_PT = 'color_point'
    COLOR_BE = 'color_bar_edge'
    HEIGHT = 'dimensions_height'
    WIDTH = 'dimensions_width'
    SIZE_TICK = 'label_size_tick'
    SIZE_AXIS = 'label_size_axis'
    LABEL = 'label_waittime'
    LEGEND = 'legend_presence'
    LWD = 'line_width'
    FORMAT = 'output_format'
    PAD = 'pad_from_axis_label_to_ticks'
    ROTATION = 'tick_rotation'
    BAR = 'type_barplot'
    HIST = 'type_histogram'
    BOX = 'type_boxplot'

    # List the remaining miscellaneous parameters.
    NEG = 'aidoc_result_negative'
    POS = 'aidoc_result_positive'
    BOOL = 'column_type_boolean'
    CAT = 'column_type_categorical'
    TRANS = 'column_transformed'
    DT_SA = 'datetime_format_for_study_aquistion'
    DT_CO = 'datetime_format_for_case_open'
    DT_MO = 'datetime_format_month'
    MONTH = 'datetime_month'
    TIME = 'datetime_time'
    SECONDS = 'datetime_seconds_in_regex'

    # Define the methods that allow for the processing of the file.
    def __init__(self, config_file=FILE):
        self.config_contents = config_file

    def read_config(self):
        """Read the file so that its parameters can be accessed.
        """

        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_contents)
        self.config_contents = config_parser

    def get_path(self, key, header=PATHS):
        """Get file parameters that relate to paths/directories.

        Args:
            key (string): key associated with the parameter of interest.
            header (string): file header within which the key is found.

        Returns:
            string: string of the parameter of interest.
        """

        return self.config_contents.get(header, key)

    def get_column_name(self, key, header=NAMES):
        """Get file parameters that relate to DataFrame column names.

        Args:
            key (string): key associated with the parameter of interest.
            header (string): file header within which the key is found.

        Returns:
            string: string of the parameter of interest.
        """

        return self.config_contents.get(header, key)

    def get_plot_param(self, key, header=PLOTS):
        """Get file parameters that relate to plot settings.

        Args:
            key (string): key associated with the parameter of interest.
            header (string): file header within which the key is found.

        Returns:
            string: string of the parameter of interest.
        """

        return self.config_contents.get(header, key)

    def get_misc(self, key, header=MISC):
        """Get file parameters that relate to miscellaneous settings.

        Args:
            key (string): key associated with the parameter of interest.
            header (string): file header within which the key is found.

        Returns:
            string: string of the parameter of interest.
        """

        return self.config_contents.get(header, key)
