
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
import csv
from plyer import filechooser
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



Window.size = (400,400)

# Global variables
# Stored information as a dictionary with the keys being the values stored from the column head.
data_per_column = {} # Column: Data of Column
can_be_float_converted = {} # 
path = ""
stat_options = {}
count_dictionary = {} # Column: Data Value: Count of Data Value
percentage_dictionary = {} # Column: Unique Data Value: Percentage Ratio of Data Value to total

# Used for calculations of float data types.
# Each dictionary is broken out by KEY: KEY: KEY: Data or List
data_per_unique_dictionary = {} # Column of Unique Values: Unique Data Value: Column to analyze: All Data From CSV file as a list
sum_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Sum: Sum
max_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Max: Max
min_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Min: Min
avg_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Avg: Avg
median_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Sum: Sum
total_records = 0 # Total Row of Records
mytext = "hello" # Only used for TESTING.  NOT USEFUL


# Declare Screens
class Startup(Screen):
    global mytext
    local = mytext
    run_this = True
    def press(self):
        global path, data_per_column, can_be_float_converted, total_records, mytext
        name = path[0]

        # Clear the input boxes
        file = open(name)
        csvreader = csv.reader(file)
        header_column = next(csvreader)
        data_list = [row for row in csvreader]
        column_count = len(header_column)
        total_records = len(data_list)
        index = 0    

        # All data from CSV file will be stored in data_per_column for processing.
        for each_column in header_column:
            data_per_column[each_column] = [0] * total_records
            for each in range(0,total_records):
                data_per_column[each_column][each] = data_list[each][index]
            index += 1

        # Checks for the ability to convert data in a column to a floating point for math purposes.
        print("Checking for ability to convert string to floating point for calculations.")
        for each in data_per_column:
            if "ID" in each or "id" in each:
                can_be_float_converted[each] = False
            else:
                can_be_float_converted[each] = self.data_type_checker(data_per_column[each])
            print(each + " = " + str(can_be_float_converted[each]))
        print()

        print(self.run_this)
        if self.run_this == True:
            self.options(can_be_float_converted)
            self.count_per_value('Item Type')
            self.percentage_ratio('Item Type')
            self.sums_per_unique('Item Type','Total Profit')
            self.min_per_unique('Item Type','Total Profit')
            self.max_per_unique('Item Type','Total Profit')
            self.avg_per_unique('Item Type','Total Profit')
            self.median_per_unique('Item Type', 'Total Profit')
        file.close()

    # Used to open csv file.
    def file_selector(self):
        global path
        path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Comma-separated Values", "*.csv")])
        print(path)
        
    # Checks if a data type can be converted to a float for math calculations. 
    def data_type_checker(self,some_list): 
        can_be_converted = True
        for each in some_list:
            try:
                float(each)
            except ValueError:
                can_be_converted = False
            if can_be_converted == False:
                return can_be_converted
        return can_be_converted

    # Determines what is stat options can be worked based on data types. Uses "can_be_float_converted" dictionary as an input.
    def options(self,some_dictionary):
        print("The following is the columns and their calculation abilities.") # This print is only used to see result.  NOT NEEDED.
        global stat_options
        for each in some_dictionary:
            if some_dictionary[each] == True:
                stat_options[each] = ["Counts Per Value", "Percentage Ratio", "Sum", "Max", "Min", "Average", "Median"]
            else:
                stat_options[each] = ["Counts Per Value", "Percentage Ratio"]
            print("Column: " + each + " can perform the following: " + str(stat_options[each])) # This print is only used to see result.  NOT NEEDED.
        print() # This print is only used to see result.  NOT NEEDED.


    # Counts each of the unique values within a column.   
    def count_per_value(self, column):
        print("The following is the count of unique values within the " + str(column) +  " column.")# This print is only used to see result.  NOT NEEDED.
        checked_list = []
        global count_dictionary
        count_dictionary[column] = {} 
        for each in data_per_column[column]:
            if each not in checked_list:
                checked_list.append(each)
                count_dictionary[column][each] = data_per_column[column].count(each)
                print("Column: " + str(column) + " " + str(each) +  " = " + str(count_dictionary[column][each])) # This print is only used to see result.  NOT NEEDED.
            else:
                continue
        print("Unique Values = " + str(len(checked_list))) # This print is only used to see result.  NOT NEEDED.
        print()# This print is only used to see result.  NOT NEEDED.
    

    # Calculates the percentage ratio per unique item of the total records.
    # CAN ONLY BE USED if count_per_value function is used FIRST.
    def percentage_ratio(self, column):
        print("The following is the percentage ration values of unique items in the " + str(column) +  " column.") # This print is only used to see result.  NOT NEEDED.
        global count_dictionary, percentage_dictionary, total_records
        percentage_dictionary[column] = {}
        for each in count_dictionary[column]:
            percentage_dictionary[column][each] = round(((count_dictionary[column][each] / total_records)*100),2)
            print("Column: " + str(column) + " Unique Value: " + str(each) + " Percentage Ratio = " + str(percentage_dictionary[column][each]) + "%") # This print is only used to see result.  NOT NEEDED.
        print() # This print is only used to see result.  NOT NEEDED.
    



    # Stores all data per column, unique_value, column_to_store into data_per_unique_dictionary for future prints and functions.
    # Prepares other dictionaries for certain values.
    def per_unique_setup(self,column,column_to_store):
        global data_per_column, data_per_unique_dictionary, sum_dictionary, max_dictionary, min_dictionary, avg_dictionary, median_dictionary
        data_per_unique_dictionary[column] = {}
        sum_dictionary[column] = {} # Column: Unique Data Value: Count of Data Value
        max_dictionary[column] = {}
        min_dictionary[column] = {}
        avg_dictionary[column] = {}
        median_dictionary[column] = {}

        checked_list = []
        for each in data_per_column[column]:
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
        for each in range(0,total_records):
            data_per_unique_dictionary[column][str(data_per_column[column][each])][column_to_store].append(float(data_per_column[column_to_store][each]))

    
    # Calculate sums per unique item.
    def sums_per_unique(self,column,column_to_sum):
        print("The following is the sum of " + str(column_to_sum) + " per unique values for the column " + str(column)) # This print is only used to see result.  NOT NEEDED.
        global data_per_unique_dictionary
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column,column_to_sum)
        for each in data_per_unique_dictionary[column]:
            sum_dictionary[column][each][column_to_sum] = round(np.sum(data_per_unique_dictionary[column][each][column_to_sum]), 2)
            print("Column = " + column + ", Unique Value = " + each + ", Sum " + str(column_to_sum) + " = " + str(sum_dictionary[column][each][column_to_sum])) # This print is only used to see result.  NOT NEEDED.
        print() # This print is only used to see result.  NOT NEEDED.

    # Calculate min per unique item.    
    def min_per_unique(self,column,column_to_min):
        print("The following is the min of " + str(column_to_min) + " per unique values for the column " + str(column)) # This print is only used to see result.  NOT NEEDED.
        global data_per_unique_dictionary
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column,column_to_min)
        for each in data_per_unique_dictionary[column]:
            min_dictionary[column][each][column_to_min] = round(min(data_per_unique_dictionary[column][each][column_to_min]), 2)
            print("Column = " + column + ", Unique Value = " + each + ", Min " + str(column_to_min) + " = " + str(min_dictionary[column][each][column_to_min])) # This print is only used to see result.  NOT NEEDED.
        print() # This print is only used to see result.  NOT NEEDED.

    # Calculates max per unique item.
    def max_per_unique(self, column, column_to_max):
        print("The following is the max of " + str(column_to_max) + " per unique values for the column " + str(column)) # This print is only used to see result.  NOT NEEDED.
        global  data_per_unique_dictionary
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column,column_to_max)
        for each in data_per_unique_dictionary[column]:
            max_dictionary[column][each][column_to_max] = round(max(data_per_unique_dictionary[column][each][column_to_max]), 2)
            print("Column = " + column + ", Unique Value = " + each + ", Max " + str(column_to_max) + " = " + str(max_dictionary[column][each][column_to_max])) # This print is only used to see result.  NOT NEEDED.
        print() # This print is only used to see result.  NOT NEEDED.


    # Calculates average per unique item.
    def avg_per_unique(self, column, column_to_average):
        print("The following is the averages of " + str(column_to_average) + " per unique values for the column " + str(column)) # This print is only used to see result.  NOT NEEDED.
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column,column_to_average)
        for each in data_per_unique_dictionary[column]:
            avg_dictionary[column][each][column_to_average] = round(np.average(data_per_unique_dictionary[column][each][column_to_average]), 2)
            print("Column = " + column + ", Unique Value = " + each + ", Average " + str(column_to_average) + " = " + str(avg_dictionary[column][each][column_to_average])) # This print is only used to see result.  NOT NEEDED.
        print()# This print is only used to see result.  NOT NEEDED.
    
    # Calculates median per unique item.
    def median_per_unique(self,column,column_to_median):
        print("The following is the sum of " + str(column_to_median) + " per unique values for the column " + str(column)) # This print is only used to see result.  NOT NEEDED.
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column,column_to_median)
        for each in data_per_unique_dictionary[column]:
            median_dictionary[column][each][column_to_median] = round(np.median(data_per_unique_dictionary[column][each][column_to_median]), 2)
            print("Column = " + column + ", Unique Value = " + each + ", Median " + str(column_to_median) + " = " + str(median_dictionary[column][each][column_to_median])) # This print is only used to see result.  NOT NEEDED.
        print() # This print is only used to see result.  NOT NEEDED.

class Display(Screen): 
    mytext = Startup.local # Only used for testing.  Not really useful.
  # Checkbox exclude null
    
    def exclude_null(self, instance, value):
        print(value)
        if value == True: # Only used for testing.  Not really useful.
            Screen.run_this = True # Only used for testing.  Not really useful.
  # Checkbox exclude outliers
    def exclude_outliers(self, instance, value):
        print("Exclude Outliers:", value)

kv_file = Builder.load_file('inputStatDesign.kv')

class MyApp(App):
    # Window Title
    title = 'QuickStat'

    def build(self):
        return ScreenManager()

if __name__ == '__main__':
    MyApp().run()



