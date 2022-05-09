"""
A app for retreiving basic statistics from a csv file.
"""
# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate

import os
import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
import csv
from plyer import filechooser
import numpy as np
import pandas as pd
from kivy.resources import resource_add_path, resource_find
from pandas.api.types import is_numeric_dtype
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader


Window.size = (400, 260)

# Global variables
FILEPATH = ''
DF = pd.DataFrame()

# Stores information as a dictionary w/ column heads as keys.
data_list = []
data_column = {}  # Column: Data of Column
can_convert = {}
path = ""
stat_options = {}
cnt_dict = {}  # Column: Data Value: Count of Data Value
perc_dict = {}  # Column: Unique Data Value: Percentage Ratio

# Used for calculations of float data types.
# Dictionaries are broken out by KEY: KEY: KEY: Data or List
data_per_unique_dictionary = {}  # Column of Unique Values: Unique Data Value: Column to analyze: Data
sum_dictionary = {}  # Column: Unique Data Values: Column to Sum: Sum
max_dictionary = {}  # Column: Unique Data Values: Column to Max: Max
min_dictionary = {}  # Column: Unique Data Values: Column to Min: Min
avg_dictionary = {}  # Column: Unique Data Values: Column to Avg: Avg
median_dictionary = {}  # Column : Unique Data Values: Column to Sum: Sum
tot_rec = 0  # Total Row of Records
column_count = 0
header_column = []
header_run = {}
calc_header_run = {}


# Declare Screens
class Startup(Screen):
    """Startup screen with buttons for csv file selection"""
    def press(self):
        global header_column

    # Used to open csv file.
    def file_selector(self):
        """Lets a user select a csv file"""
        global path, header_column, data_list, column_count, tot_rec, index, data_column, can_convert, header_run, calc_header_run
        header_run.clear()
        calc_header_run.clear()
        path = filechooser.open_file(title="Pick a CSV file..", filters=[("Comma-separated Values", "*.csv", ".xlsm")])
        name = path[0]
        file = open(name)
        csvreader = csv.reader(file)
        header_column = next(csvreader)
        data_list = [row for row in csvreader]
        column_count = len(header_column)
        tot_rec = len(data_list)

        # Data from CSV file will be stored in data_per_column.
        index = 0
        for each_column in header_column:
            data_column[each_column] = [0] * tot_rec
            for each in range(0, tot_rec):
                data_column[each_column][each] = data_list[each][index]
            index += 1

        # Checks ability to convert data to floating point.
        for each in data_column:
            if "ID" in each or "id" in each:
                can_convert[each] = False
            else:
                can_convert[each] = self.data_type_checker(data_column[each])
        file.close()

    # Converted to a float for math calculations.
    def data_type_checker(self, some_list):
        can_be_converted = True
        for each in some_list:
            try:
                float(each)
            except ValueError:
                can_be_converted = False
            if can_be_converted is False:
                return can_be_converted
        return can_be_converted


class Display_1(Screen):
    global can_convert, header_run

    def switchScreens(self, value):
        if self.manager.current == 'display_1':
            self.manager.current = 'display_2'
            self.manager.transition.direction = "right"
            self.clear_up_page()

    def checkbox_function(self, checkbox, value):
        return value

    def data_fill(self):
        global header_column, header_run

        grid = GridLayout(cols=1)
        go_back = Button(text="Next", font_size=24)
        go_back.bind(on_press=self.switchScreens)
        grid1 = GridLayout(cols=2)
        grid1.add_widget(Label(text='Group By', font_size=24))
        grid1.add_widget(go_back)
        for each in header_column:
            if can_convert[each] is False:
                grid1.add_widget(Label(text=each))
                header_run[each] = CheckBox()
                header_run[each].bind(active=self.checkbox_function)
                grid1.add_widget(header_run[each])
        grid.add_widget(grid1)
        self.add_widget(grid)

    def clear_up_page(self):
        self.clear_widgets()


class Display_2(Screen):
    global can_convert, calc_header_run

    def go_next_function(self, value):
        if self.manager.current == 'display_2':
            # Window.fullscreen = 'auto'
            self.manager.current = 'display_3'
            self.manager.transition.direction = "right"
            self.clear_up_page()

    def checkbox_function(self, checkbox, value):
        return value

    def data_fill(self):
        global header_column, calc_header_run
        grid = GridLayout(cols=1)
        go_back = Button(text="Finished",
                         font_size=24,
                         color=(0, 0, 0, 1),
                         background_normal='',
                         background_color=(0, .6, 0, 1))
        go_back.bind(on_press=self.go_next_function)
        grid1 = GridLayout(cols=2)
        grid1.add_widget(Label(text='Calculatable', font_size=24))
        grid1.add_widget(go_back)
        for each in header_column:
            if can_convert[each] is True:
                grid1.add_widget(Label(text=each))
                calc_header_run[each] = CheckBox()
                calc_header_run[each].bind(active=self.checkbox_function)
                grid1.add_widget(calc_header_run[each])
        grid.add_widget(grid1)
        self.add_widget(grid)

    def clear_up_page(self):
        self.clear_widgets()


# Data Analysis screen/window
class Display_3(Screen):
    """Screen for displaying statistics from given csv file."""
    global data_column, data_per_unique_dictionary, sum_dictionary
    global max_dictionary, min_dictionary, avg_dictionary, median_dictionary
    global header_run

    def switchScreens(self, value):
        """Switch from display screen to startup screen."""
        if self.manager.current == 'display_3':
            self.manager.current = 'startup'
            self.manager.transition.direction = "right"
            Window.fullscreen = False
            Window.size = (400, 400)
            self.clear_up_page()

    def clear_up_page(self):
        self.clear_widgets()

    def build_columns_as_tabs(self):
        """Create, populate & add tabbed_panel"""
        global path
        global DF0
        DF = pd.read_csv(path[0])
        tp = TabbedPanel()
        tp.do_default_tab = False
        for column_header in header_run:
            if (header_run[column_header].active is True):
                th = TabbedPanelHeader(text=column_header)
                tp.add_widget(th)
                root = ScrollView(size_hint=(1, None),
                                  size=(Window.width, Window.height))
                layout = GridLayout(cols=6, size_hint_x=1,
                                    size_hint_y=None,
                                    row_force_default=True,
                                    row_default_height=40)
                layout.bind(minimum_height=layout.setter('height'))
                result = self.count_per_value(column_header)
                for calc_column_header in calc_header_run:
                    if (calc_header_run[calc_column_header].active is True):
                        self.per_unique_setup(column_header,
                                              calc_column_header)
                        temp_list = self.calcs_per_unique(column_header,
                                                          calc_column_header)
                        for each in temp_list:
                            result.append(each)
                for each in result:
                    layout.add_widget(each)
                root.add_widget(layout)
                th.content = root
        for calc_column_header in calc_header_run:
            if (calc_header_run[calc_column_header].active is True):
                th = TabbedPanelHeader(text=calc_column_header)
                tp.add_widget(th)
                result = str(DF[calc_column_header].describe())
                new_label_calc = Label(text=result,
                                       halign='left',
                                       font_size=32)
                th.content = new_label_calc

        # Add back button to bottom of display screen
        grid = GridLayout(cols=1)
        back_btn = Button(text="Select Another Data Set",
                          size_hint_y=None,
                          height=50)
        back_btn.bind(on_press=self.switchScreens)
        grid.add_widget(tp)
        grid.add_widget(back_btn)
        self.add_widget(grid)

    def count_per_value(self, column):
        checked_list = []
        global cnt_dict, perc_dict, tot_rec
        cnt_dict[column] = {}
        perc_dict[column] = {}
        result = []
        temp_string = ""

        for each in range(2):
            result.append(Label(text=""))
        result.append(Label(text="Counts & Perctentage Ratios Per " + column,
                            font_size=24,
                            halign='left'))
        for each in range(3):
            result.append(Label(text=""))
        for each in data_column[column]:
            if each not in checked_list:
                checked_list.append(each)
                cnt_dict[column][each] = data_column[column].count(each)
                perc_val = ((cnt_dict[column][each] / tot_rec) * 100)
                perc_dict[column][each] = round(perc_val, 2)
                result.append(Label(text=each))
                temp_string = "Count = " + str(cnt_dict[column][each])
                result.append(Label(text=(temp_string)))
                temp_string = "Percentage Ratio = "
                temp_string += str(perc_dict[column][each]) + "%"
                result.append(Label(text=(temp_string),
                                    halign='left'))
                result.append(Label(text=""))
                result.append(Label(text=""))
                result.append(Label(text=""))
            else:
                continue
        return result

    # Stores all data per column, unique_value, column_to_store into
    # data_per_unique_dictionary for future prints and functions.
    # Prepares other dictionaries for certain values.
    def per_unique_setup(self, column, column_to_store):
        global data_column, data_per_unique_dictionary
        global sum_dictionary, max_dictionary, min_dictionary
        global avg_dictionary, median_dictionary
        data_per_unique_dictionary[column] = {}
        sum_dictionary[column] = {}
        max_dictionary[column] = {}
        min_dictionary[column] = {}
        avg_dictionary[column] = {}
        median_dictionary[column] = {}
        checked_list = []
        for each in data_column[column]:
            if each not in checked_list:
                checked_list.append(each)
                data_per_unique_dictionary[column][each] = {}
                sum_dictionary[column][each] = {}
                max_dictionary[column][each] = {}
                min_dictionary[column][each] = {}
                avg_dictionary[column][each] = {}
                median_dictionary[column][each] = {}

                data_per_unique_dictionary[column][each][column_to_store] = []
                sum_dictionary[column][each][column_to_store] = []
                max_dictionary[column][each][column_to_store] = []
                min_dictionary[column][each][column_to_store] = []
                avg_dictionary[column][each][column_to_store] = []
                median_dictionary[column][each][column_to_store] = []
            else:
                continue
        for each in range(0, tot_rec):
            value_1 = str(data_column[column][each])
            value_2 = column_to_store
            value = float(data_column[column_to_store][each])
            data_per_unique_dictionary[column][value_1][value_2].append(value)

    # Calculate sums per unique item.
    def calcs_per_unique(self, column, column_to_stat):
        global data_per_unique_dictionary
        result = []
        for each in range(2):
            result.append(Label(text=""))
        temp_string = "Sum, Min, Max, Average, & Median Per "
        temp_string += column
        temp_string += " for the column " + column_to_stat
        result.append(Label(text=temp_string, font_size=24))
        for each in range(3):
            result.append(Label(text=""))
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column, column_to_stat)
        for each in data_per_unique_dictionary[column]:
            temp_float = round(np.sum(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            sum_dictionary[column][each][column_to_stat] = temp_float
            temp_float = round(min(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            min_dictionary[column][each][column_to_stat] = temp_float
            max_dictionary[column][each][column_to_stat] = round(max(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            avg_dictionary[column][each][column_to_stat] = round(np.average(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            median_dictionary[column][each][column_to_stat] = round(np.median(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            result.append(Label(text=str(each)))
            result.append(Label(text=("Sum = " + str(sum_dictionary[column][each][column_to_stat])), halign='left'))
            result.append(Label(text=("Min = " + str(min_dictionary[column][each][column_to_stat])), halign='left'))
            result.append(Label(text=("Max = " + str(max_dictionary[column][each][column_to_stat])), halign='left'))
            result.append(Label(text=("Average = " + str(avg_dictionary[column][each][column_to_stat])), halign='left'))
            result.append(Label(text=("Median = " + str(median_dictionary[column][each][column_to_stat])), halign='left'))
        return result


kv_file = Builder.load_file('quickStat.kv')


class Manager(ScreenManager):
    pass


class MyApp(App):
    # Window Title
    title = 'QuickStat'

    def build(self):
        """Builds the app"""
        m = Manager()
        return m


if __name__ == '__main__':
    MyApp().run()