from kivymd.app import MDApp
from assets.data.color_definitions import colors
from Screens.GameScreen.game import GameScreen
from Screens.HomeScreen.home import HomeScreen
from Screens.RootScreen.root import RootScreen
from Screens.SettingsScreen.settings import SettingsScreen
from Utils.theme_manager import ThemeManager


class TicTacToe(MDApp):
    def build(self):
        self.title = "TicTacToe"
        self.load_all_kv_files("Screens")
        self.theme = ThemeManager(colors)
        return RootScreen()


if __name__ == "__main__":
    TicTacToe().run()