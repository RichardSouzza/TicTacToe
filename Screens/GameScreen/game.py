from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_hex_from_color

import numpy as np
from Screens.GameScreen.components.line import Line
from Screens.GameScreen.components.shadow import Shadow
from Screens.GameScreen.components.square import Square


class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.players = ["X", "O"]
        self.current_player = self.players[0]
        self.board_size = 3
        Clock.schedule_once(self.build)
    
    def build(self, *args, **kwargs):
        try:
            self.board_size = kwargs["board_size"]
        except KeyError:
            pass
        
        self.current_player = self.players[0]
        self.ids.board.clear_widgets()
        self.ids.board.cols = self.board_size
        
        for col in range(self.board_size):
            for row in range(self.board_size):
                self.ids.board.add_widget(Square())
        
        color = self.get_markup_color()
        self.ids.cp_label.text = f"[color={color}]{self.current_player}[/color] Turn!"
        
        if self.board_size == 3:
            self.marks = 3
        elif 3 < self.board_size < 9:
            self.marks = 4
        elif 9 <= self.board_size < 11:
            self.marks = 5
        else:
            self.marks = 6
    
    def change_player(self):
        self.check_victory()
        for player in self.players:
            if player != self.current_player:
                self.current_player = player
                break
        color = self.get_markup_color()
        self.ids.cp_label.text = f"[color={color}]{self.current_player}[/color] Turn!"
    
    def check_victory(self):
        def get_text_from_array(array):
            return "".join([square.text for square in array])
        
        def victory_check(line):
            return "X" * self.marks in line or "O" * self.marks in line
        
        squares_list = [square for square in self.squares()]
        grid = self.get_grid(squares_list)
        
        for col in grid.T:
            line = get_text_from_array(col)
            if victory_check(line):
                self.victory("vertical", col)
        
        for row in grid:
            line = get_text_from_array(row)
            if victory_check(line):
                self.victory("horizontal", row)
        
        for diagonal in self.get_diagonals(grid):
            if victory_check(get_text_from_array(diagonal)):
                self.victory("diagonal1", diagonal)
        
        for diagonal in self.get_diagonals(np.fliplr(grid)):
            if victory_check(get_text_from_array(diagonal)):
                self.victory("diagonal2", diagonal)
        
        if (" " not in get_text_from_array(grid.ravel()) and
            Shadow not in [type(widget) for widget in self.walk()]):
            self.draw()
    
    def draw(self):
        shadow = Shadow()
        shadow.ids.win_label.text = "Draw!"
        self.add_widget(shadow)
        
        animation1 = Animation(
            opacity=1,
            duration=.3,
        )
        animation2 = Animation(
            opacity=1,
            duration=.3,
        )
        animation3 = Animation(
            opacity=0,
            duration=.3
        )
        animation1.bind(on_complete=lambda *args: animation2.start(shadow.ids.win_label))
        animation1.bind(on_complete=lambda *args: animation2.start(shadow.ids.play_label))
        animation1.start(shadow)
        animation3.start(self.ids.cp_label)
    
    def get_diagonals(self, grid):
        count = self.board_size * -1 +1
        while count < self.board_size:
            yield grid.diagonal(offset=count)
            count += 1
    
    def get_grid(self, squares_list):
        cols = self.board_size
        rows = self.board_size
        index = 0
        grid = [[] for row in range(rows)]
        for count, square in enumerate(squares_list):
            grid[index].append(square)
            if count + 1 == cols * (index + 1):
                index += 1
        grid = np.array(grid)
        return grid
    
    def get_markup_color(self):
        if self.current_player == "X":
            return get_hex_from_color(self.app.theme.cross_color)
        else:
            return get_hex_from_color(self.app.theme.circle_color)
    
    @staticmethod
    def remove_spaces(list):
        return [item for item in list if item != " "]
    
    def restart(self):
        def clear_screen():
            for widget in self.walk():
                if type(widget) == Square:
                    widget.text = " "
                    widget.ids.label.opacity = 1
                
                elif type(widget) in (Line, Shadow):
                    self.remove_widget(widget)
        
        animation = Animation(
            opacity=0,
            duration=.3
        )
        
        self.ids.cp_label.opacity = 1
        callback = animation.bind(on_complete=lambda *args: clear_screen())
        
        for widget in self.walk():
            if type(widget) == Square:
                animation.start(widget.ids.label)
            elif type(widget) in (Line, Shadow):
                animation.start(widget)
    
    def squares(self):
        for widget in self.walk():
            if type(widget) == Square:
                yield widget
    
    def victory(self, direction, sequence):
        # Remove empty squares:
        sequence = [square for square in sequence if square.text != " "]
        
        # Draw line:
        x1, y1 = sequence[0].center_x, sequence[0].center_y
        x2, y2 = sequence[-1].center_x, sequence[-1].center_y
        increment_x = self.ids.board.col_default_width / 2
        increment_y = self.ids.board.row_default_height / 2
        
        if direction == "horizontal":
            x1 -= increment_x
            x2 += increment_x
        
        elif direction == "vertical":
            y1 += increment_y
            y2 -= increment_y
        
        elif direction == "diagonal1":
            x1 -= increment_x
            x2 += increment_x
            y1 += increment_y
            y2 -= increment_y
        
        elif direction == "diagonal2":
            x1 += increment_x
            x2 -= increment_x
            y1 += increment_y
            y2 -= increment_y
        
        line = Line(
            coordinates=[x1, y1, x1, y1],
            _width=dp(10) / self.board_size * 3
        )
        
        self.ids.box.add_widget(line)
        
        animation1 = Animation(
            coordinates=[x1, y1, x2, y2],
            duration=.2
        ).start(line)
        
        if Shadow not in [type(widget) for widget in self.walk()]:
            # Show victory screen:
            color = self.get_markup_color()
            shadow = Shadow()
            shadow.ids.win_label.text = f"[color={color}]{self.current_player}[/color] Wins!"
            self.add_widget(shadow)
            
            animation2 = Animation(
                duration=.6
            ) + Animation(
                opacity=1,
                duration=.3,
            )
            animation3 = Animation(
                opacity=1,
                duration=.3
            )
            animation4 = Animation(
                opacity=0,
                duration=.3
            )
            animation2.bind(on_complete=lambda *args: animation3.start(shadow.ids.win_label))
            animation2.bind(on_complete=lambda *args: animation3.start(shadow.ids.play_label))
            animation2.start(shadow)
            animation4.start(self.ids.cp_label)
