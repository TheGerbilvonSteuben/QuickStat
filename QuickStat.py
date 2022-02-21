import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyGridLayout(Widget):
    def press(self):
        print("Button has been pressed!")

class QuickStat(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    QuickStat().run()