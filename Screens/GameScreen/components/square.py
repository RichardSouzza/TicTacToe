from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty


class Square(MDRelativeLayout):
    text = StringProperty(" ")
    
    def __init__(self, **kwargs):
        super(Square, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def mark(self):
        if self.text == " ":
            root = self.app.root.current_screen
            self.text = root.current_player
            root.change_player()
