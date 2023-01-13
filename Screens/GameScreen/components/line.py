from kivymd.uix.widget import MDWidget
from kivy.properties import ListProperty, NumericProperty


class Line(MDWidget):
    coordinates = ListProperty()
    _width = NumericProperty()
