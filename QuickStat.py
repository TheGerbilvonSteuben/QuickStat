# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from plyer import filechooser
from kivy.uix.screenmanager import ScreenManager, Screen

# Declare Screens
# Main window. Option to choose a dataset.
class first_window(Screen):
  pass

# Second window. Data Analysis Screen with several options
class second_window(Screen):
  # Get the csv file
  def file_chooser(self):
    path = filechooser.open_file(title="Pick a CSV file..", filters=[("Comma-separated Values", "*.csv")])
    print(path)

  # Checkbox exclude null
  def exclude_null(self, instance, value):
    print("Exclude Null:", value)
  
  # Checkbox exclude outliers
  def exclude_outliers(self, instance, value):
    print("Exclude Outliers:", value)
    
  pass

# Set the app size
Window.size = (800,800)

# Designate Our .kv design file 
kv = Builder.load_file('QuickStatStart.kv')
    

      
class QuickStat(App):
  # Window Title
  title = 'QuickStat'
  
  def build(self):
    # Create the screen manager
    sm = ScreenManager()
    sm.add_widget(first_window(name = 'first'))
    sm.add_widget(second_window(name = 'second'))

    
    
    return sm

if __name__ == '__main__':
    QuickStat().run()
