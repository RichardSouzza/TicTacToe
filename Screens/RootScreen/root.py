from kivymd.uix.screen import MDScreen


class RootScreen(MDScreen):
    def change_screen(self, screen, direction="left"):
        self.ids.screen_manager.transition.direction = direction
        self.ids.screen_manager.current = screen
    
    @property
    def current_screen(self):
        return self.ids.screen_manager.current_screen
    
    def get_screen(self, name):
        return self.ids.screen_manager.get_screen(name)
