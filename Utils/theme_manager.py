from kivy.utils import get_color_from_hex as hex


class ThemeManager:
    def __init__(self, palette):
        self.palette = self.hex_to_color(palette)
        self.bg_color = self.palette["Gray"]["200"]
        self.circle_color = self.palette["Blue"]["500"]
        self.cross_color = self.palette["Red"]["500"]
        self.primary_color = self.palette["Gray"]["600"]
        self.primary_light = self.palette["Gray"]["400"]
        self.primary_dark = self.palette["Gray"]["800"]
    
    @staticmethod
    def hex_to_color(colors):
        palette = {}
        for color, hues in colors.items():
            palette[color] = {}
            for hue, code in hues.items():
                palette[color][hue] = hex(code)
        
        return palette
