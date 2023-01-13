from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty


class TextButton(MDBoxLayout):
    text = StringProperty(" ")
    link = StringProperty()
