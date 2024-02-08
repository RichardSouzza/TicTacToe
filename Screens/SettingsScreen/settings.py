from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from Utils.config import get_config, set_config


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        Clock.schedule_once(self.build)
    
    def build(self, *args):
        self.ids["slider"].value = get_config("board")["board_size"]
    
    def update_settings(self):
        game = self.app.root.get_screen("game")
        new_board_size = self.ids["slider"].value
        if new_board_size != game.board_size:
            set_config("board_size", new_board_size)
            if new_board_size == 3:
                set_config("winning_condition", 3)
            elif 3 < new_board_size < 9:
                set_config("winning_condition", 4)
            elif 9 <= new_board_size < 11:
                set_config("winning_condition", 5)
            else:
                set_config("winning_condition", 6)
            game.build()
