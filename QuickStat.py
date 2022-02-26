# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate


from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from plyer import filechooser
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd


# Set the app size
Window.size = (800,800)

# Global variables
filepath = ''
df = pd.DataFrame()
# Declare Screens

# Main window. Choose a dataset.
class Startup(Screen):
  # Get the csv file
  def file_chooser(self):
    global filepath 
    filepath = filechooser.open_file(title="Pick a CSV file..", filters=[("Comma-separated Values", "*.csv")])
    print(filepath)


# Second window. Data Analysis Screen with several options
class Display(Screen):
  
  # Create dataframe from selected csv
  def createdf(self):
    global filepath
    global df 
    df = pd.read_csv(filepath[0])
    print(df.head)

  # Checkbox exclude null
  def exclude_null(self, instance, value):
    print("Exclude Null:", value)
  
  # Checkbox exclude outliers
  def exclude_outliers(self, instance, value):
    print("Exclude Outliers:", value)


# Designate Our .kv design file 
kv_file = Builder.load_file('quickStatDesign.kv')


class QuickStat(App):
  # Window Title
  title = 'QuickStat'
  
  def build(self):
    
    return ScreenManager()

if __name__ == '__main__':
    QuickStat().run()
