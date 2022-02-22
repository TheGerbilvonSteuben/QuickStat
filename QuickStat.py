# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

#run this everytime in command.com
# kivy_venv\Scripts\activate


from cgitb import text
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config 

from kivy.uix.gridlayout import GridLayout


from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label

from plyer import filechooser

# Set the app size
Window.size = (800,800)

# Full screen app
#Window.fullscreen = True
#Window.maximize()

# Designate Our .kv design file 
Builder.load_file('QuickStat.kv')

# Need to check if we still need this
class myLayout(GridLayout):
  def __init__(self, **kwargs):
    super(GridLayout, self).__init__(**kwargs)

    
  # clickity clack action
  def press(self):
    path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Comma-separated Values", "*.csv")])
    print(path)


      
class Main(App):
  # Window Title
  title = 'QuickStat'
  
  def build(self):
    return myLayout()

if __name__ == '__main__':
    Main().run()