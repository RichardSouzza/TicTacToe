from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def set_board_size(self):
        game = self.app.root.get_screen("game")
        value = self.ids["slider"].value
        if value != game.board_size:
            game.build(board_size=value)
