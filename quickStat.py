"""
A app for retreiving statistics from a csv file.
"""
# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate

from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import filechooser
import pandas as pd
from pandas.api.types import is_numeric_dtype
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader


# Set the app size
Window.size = (400, 260)

# Global variables
FILEPATH = ''
DF = pd.DataFrame()


# Main screen/window.
class Startup(Screen):
    """Startup screen with buttons for csv file selection"""
    # Get the csv file
    def file_chooser(self):
        """Lets a user select a csv file"""
        global FILEPATH
        FILEPATH = filechooser.open_file(
            title="Pick a CSV file..",
            filters=[("Comma-separated Values", "*.csv")])
        # print(FILEPATH)


# Data Analysis screen/window
class Display(Screen):
    """Screen for displaying statistics from given csv file."""

    def build_columns_as_tabs(self):
        """Create, populate & add tabbed_panel"""
        global FILEPATH
        global DF
        DF = pd.read_csv(FILEPATH[0])
        # print(DF)
        tp = TabbedPanel()
        tp.do_default_tab = False

        new_line = "\n"
        new_para = "\n\n"

        for col_name in DF:
            col = DF[col_name]
            th = TabbedPanelHeader(text=col_name)
            tp.add_widget(th)

            is_num = is_numeric_dtype(col)

            # list to be used for str.join
            stat_string_list = []

            count_string = "Count: " + str(col.count())
            stat_string_list.append(count_string)
            stat_string_list.append(new_para)

            unique_count_string = ("Unique count: " + new_line +
                                   str(col.value_counts().nlargest(5)))
            stat_string_list.append(unique_count_string)
            stat_string_list.append(new_para)

            if is_num:
                mean_string = "Mean: " + str(col.mean())
                stat_string_list.append(mean_string)
                stat_string_list.append(new_para)

                median_string = "Median: " + str(col.median())
                stat_string_list.append(median_string)
                stat_string_list.append(new_para)

            # Make the final string
            stat_string = ''.join(stat_string_list)
            th.content = Label(text=stat_string)

        self.add_widget(tp)


class QuickStat(App):
    """Main application"""
    # Window Title
    title = 'QuickStat'

    def build(self):
        """Builds the app"""
        return ScreenManager()


if __name__ == '__main__':
    QuickStat().run()
