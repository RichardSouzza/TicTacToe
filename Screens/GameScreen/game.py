from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_hex_from_color

from Screens.GameScreen.components.line import Line
from Screens.GameScreen.components.shadow import Shadow
from Screens.GameScreen.components.square import Square
from Utils.config import get_config


class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.players = ["X", "O"]
        Clock.schedule_once(self.build)
    
    def build(self, *args):
        config = get_config("board")
        self.board_size = config["board_size"]
        self.winning_condition = config["winning_condition"]
        self.current_player = self.players[0]
        self.set_current_player_label()
        self.ids.board.clear_widgets()
        self.ids.board.cols = self.board_size
        self.board = []
        self.grid = []

        for row in range(self.board_size):
            self.board.append([])
            for col in range(self.board_size):
                square = Square()
                self.ids.board.add_widget(square)
                self.board[row].append(square)
    
    def get_row(self, x, y, length):
        row = self.grid[y][x:x+length]
        return row

    def get_col(self, x, y, length):
        col = [row[x] for row in self.grid[y:y+length]]
        return col

    def get_diag(self, x, y, length):
        diag = []
        for len in range(length):
            try:
                diag.append(self.grid[y][x])
            except IndexError:
                break
            x += 1
            y += 1
        return diag
    
    def get_anti_diag(self, x, y, length):
        anti_diag = []
        len = 0
        while len <= length and y >= 0:
            try:
                anti_diag.append(self.grid[y][x])
            except IndexError:
                break
            x += 1
            y -= 1
        return anti_diag

    def check_victory(self):
        winning_combination = [self.current_player * self.winning_condition]
        check_combination = lambda combination : combination in winning_combination
        winning_lines = []
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                row_line = col_line = diag_line = anti_diag_line = None

                if self.board_size - self.winning_condition >= col:
                    row_line = "".join(self.get_row(col, row, self.winning_condition))
                if self.board_size - self.winning_condition >= row:
                    col_line = "".join(self.get_col(col, row, self.winning_condition))
                if row_line and col_line:
                    diag_line = "".join(self.get_diag(col, row, self.winning_condition))
                if row >= self.winning_condition - 1 and row_line:
                    anti_diag_line = "".join(self.get_anti_diag(col, row, self.winning_condition))

                if check_combination(row_line): 
                    winning_lines.append((
                        col, row,
                        col + self.winning_condition - 1, row
                    ))
                if check_combination(col_line): 
                    winning_lines.append((
                        col, row,
                        col, row + self.winning_condition - 1
                    ))
                if check_combination(diag_line): 
                    winning_lines.append((
                        col, row,
                        col + self.winning_condition - 1, row + self.winning_condition - 1
                    ))
                if check_combination(anti_diag_line):
                    winning_lines.append((
                        col, row,
                        col + self.winning_condition - 1, row - self.winning_condition + 1
                    ))
        
        if any(winning_lines):
            for line in winning_lines:
                self.victory(line)
        elif " " not in sum(self.grid, []):
            self.draw()
    
    def set_grid(self):
        self.grid = []
        for y, row in enumerate(self.board):
            self.grid.append([])
            for square in row:
                self.grid[y].append(square.text)
    
    def turn_handler(self):
        self.set_grid()
        self.check_victory()
        self.current_player = self.players[
            (self.players.index(self.current_player) + 1) % len(self.players)]
        self.set_current_player_label()

    def set_current_player_label(self):
        color = self.get_markup_color()
        self.ids.current_player_label.text = f"[color={color}]{self.current_player}[/color] Turn!"

    def get_markup_color(self):
        markup_colors = {
            "X": self.app.theme.cross_color,
            "O": self.app.theme.circle_color,
        }
        return get_hex_from_color(markup_colors[self.current_player])
    
    def get_square_coordinates(self, square):
        return square.center_x, square.center_y

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
        animation3.start(self.ids.current_player_label)
    
    def victory(self, line):
        lx1, ly1, lx2, ly2 = line
        start = self.board[ly1][lx1]
        end = self.board[ly2][lx2]
        x1, y1 = self.get_square_coordinates(start)
        x2, y2 = self.get_square_coordinates(end)
        increment_x = self.ids.board.col_default_width / 2
        increment_y = self.ids.board.row_default_height / 2

        if ly1 == ly2:
            x1 -= increment_x
            x2 += increment_x
        
        elif lx1 == lx2:
            y1 += increment_y
            y2 -= increment_y
        
        elif lx1 == ly1 and lx2 == ly2:
            x1 -= increment_x
            x2 += increment_x
            y1 += increment_y
            y2 -= increment_y
        
        elif lx1 == ly2 and ly1 == lx2:
            x1 -= increment_x
            x2 += increment_x
            y1 -= increment_y
            y2 += increment_y
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        line = Line(
            coordinates=[x1, y1, x1, y1],
            _width=dp(8) / self.board_size * 3
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
            animation4.start(self.ids.current_player_label)
    
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
        
        self.ids.current_player_label.opacity = 1
        callback = animation.bind(on_complete=lambda *args: clear_screen())
        
        for widget in self.walk():
            if type(widget) == Square:
                animation.start(widget.ids.label)
            elif type(widget) in (Line, Shadow):
                animation.start(widget)
