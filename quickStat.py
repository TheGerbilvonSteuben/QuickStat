"""
A app for retreiving statistics from a csv file.
"""
# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate

from kivy.app import App
from kivy.core.window import Window
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
        for column_header in DF:
            th = TabbedPanelHeader(text=column_header)
            tp.add_widget(th)
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
