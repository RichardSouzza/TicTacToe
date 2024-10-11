from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.core.window import Window


class RootScreen(MDScreen):
    def __init__(self, **kwargs):
        super(RootScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        Clock.schedule_once(lambda x: Window.bind(on_keyboard=self.handle_actions))

    def change_screen(self, screen, direction="left"):
        self.ids.screen_manager.transition.direction = direction
        self.ids.screen_manager.current = screen
    
    @property
    def current_screen(self):
        return self.ids.screen_manager.current_screen
    
    def get_screen(self, name):
        return self.ids.screen_manager.get_screen(name)
    
    def handle_actions(self, window, key, *args):
        if key == 27: # Esc
            if self.current_screen.name != "home":
                self.change_screen("home", "right")
                return True
