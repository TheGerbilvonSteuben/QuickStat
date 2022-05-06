"""
A app for retreiving basic statistics from a csv file.
"""
# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate

import os
import sys
from kivy.resources import resource_add_path, resource_find
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
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
            title="Pick a CSV or XMLS file..",
            filters=[("Comma-separated Values", "Microsoft Excel Worksheet", "*.csv", "*.xlsm")])


# Data Analysis screen/window
class Display(Screen):
    """Screen for displaying statistics from given csv file."""
    def switchScreens(self, value):
        """Switch from display screen to startup screen."""
        if self.manager.current == 'display':
            self.manager.current = 'startup'
            self.manager.transition.direction = "right"

    def build_columns_as_tabs(self):
        """Create, populate & add tabbed_panel."""
        global FILEPATH
        global DF

        # Differentiate between diffrent kinds of csv files
        if ".xlsm" in FILEPATH[0]:
            DF = pd.read_excel(FILEPATH[0])
        else:
            DF = pd.read_csv(FILEPATH[0])
        # Clear any preexisting widgets
        # from previously opened csv files
        self.clear_widgets()

        # Begin creating tabs
        grid = GridLayout(cols=2)
        tp = TabbedPanel()
        tp.do_default_tab = False

        for col_name in DF:
            col = DF[col_name]
            is_num = is_numeric_dtype(col)
            if is_num:
                th = TabbedPanelHeader(text=col_name)
                grid.add_widget(Label(text="Number of entries: "
                                + str(col.count())))
                grid.add_widget(Label(text="Mean: "
                                + str(col.mean())))
                grid.add_widget(Label(text="Median: "
                                + str(col.median())))
                grid.add_widget(Label(text="Max: "
                                + str(col.max())))
                grid.add_widget(Label(text="Min: "
                                + str(col.min())))
                th.content = grid
                tp.add_widget(th)
                grid = GridLayout(cols=2)

        # Add back button to bottom of display screen
        grid = GridLayout(cols=1)
        back_btn = Button(text="Select Another Data Set")
        back_btn.bind(on_press=self.switchScreens)
        grid.add_widget(tp)
        grid.add_widget(back_btn)
        self.add_widget(grid)


class Manager(ScreenManager):
    pass


class QuickStat(App):
    """Main application"""
    # Window Title
    title = 'QuickStat'

    def build(self):
        """Builds the app"""
        m = Manager()
        return m


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = QuickStat()
        app.run()
    except Exception as e:
        print(e)
        input("Press enter.")
