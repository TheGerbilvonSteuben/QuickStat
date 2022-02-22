from cgitb import text
from kivy.app import App
from kivy.config import Config 
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from plyer import filechooser

# Set the app size
Window.size = (800,800)

# Designate Our .kv design file 
Builder.load_file('QuickStatStart.kv')

class myLayout(Widget):
    
  # Get the csv file
  def press(self):
    path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Comma-separated Values", "*.csv")])
    print(path)

      
class QuickStat(App):
  # Window Title
  title = 'QuickStat'
  
  def build(self):
    return myLayout()

if __name__ == '__main__':
    QuickStat().run()
