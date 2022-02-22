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

# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 
Config.set('graphics', 'resizable', True)

# Full screen app
#Window.fullscreen = True
#Window.maximize()

# # Designate Our .kv design file 
# Builder.load_file('QuickStat.kv')

class GridLayout(GridLayout):
  def __init__(self, **kwargs):
    super(GridLayout, self).__init__(**kwargs)

    # Need to set it as 1 for properly displaying output
    self. cols = 1

    # (+) Open File 
    self.PLUS_BUTTON = Button(text="Open File", font_size = 32, pos = (20,20))
    # bind the button
    self.PLUS_BUTTON.bind(on_press = self.press)
    # add the button
    self.add_widget(self.PLUS_BUTTON)

    # Footer
    self.add_widget(Label(text='© QuickStat Team. All Rights Reserved.', font_size = 20))

  def press(self, instance):
    path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Comma-separated Values", "*.csv")])
    print(path)



    


      
class Main(App):
  # Window Title
  title = 'QuickStat'
  
  def build(self):
    return GridLayout()

if __name__ == '__main__':
    Main().run()