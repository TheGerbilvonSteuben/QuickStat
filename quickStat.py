"""
A app for retreiving statistics from a csv file.
"""
# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import filechooser
import pandas as pd
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
        print(FILEPATH)


# Data Analysis screen/window
class Display(Screen):
    """Screen for displaying statistics from given csv file."""

    # def add_widget(self, widget, *args, **kwargs):
    #     return super().add_widget(widget, *args, **kwargs)

    # TODO: the 2nd Screen is currently showing as blank
    # make it display the tabbedpanel in Display Screen
    # the two print statements imply that:
    #       1. df is correctly created
    #       2. tp seems to have been populated
    def build_columns_as_tabs(self):
        global FILEPATH
        global DF
        DF = pd.read_csv(FILEPATH[0])
        # print(DF.head())
        tp = TabbedPanel()
        for column_header in DF:
            # print(column_header)
            th = TabbedPanelHeader(text=column_header)
            tp.add_widget(th)
        # print(tp.tab_list)

        # Display.add_widget(tp)


# Designate Our .kv design file
kv_file = Builder.load_file('quickStatDesign.kv')


class QuickStat(App):
    """Main application"""
    # Window Title
    title = 'QuickStat'

    def build(self):
        """Builds the app"""
        return ScreenManager()


if __name__ == '__main__':
    QuickStat().run()
