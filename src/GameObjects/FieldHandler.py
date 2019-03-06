from src.GameObjects.GameObjects import ChessSquare, Bauer
import pygame


class FieldHandler:

    def __init__(self):
        self.black = (255, 255, 255)
        self.white = (0, 0, 0)
        self.width = 100
        self.height = 100
        self.black_or_white = 0
        self.field = []
        self.player_field = []

    def setup_draw(self, background):
        x_pos, y_pos = 0, 0
        for y in range(0, 8):
            row = []
            for x in range(0, 8):
                color = self.color()
                rect = ChessSquare(x_pos, y_pos, color, self.width, self.height, 0)
                pygame.draw.rect(background, rect.color, rect.rect, rect.thickness)
                row.append(rect)
                x_pos += 100
            self.color_swap()
            x_pos = 0
            y_pos += 100
            self.field.append(row)
        self._setup_player_field(background)

    def draw(self, background):
        for row in self.field:
            for rect in row:
                pygame.draw.rect(background, rect.color, rect.rect, rect.thickness)

    def draw_board(self, background):
        for row in self.player_field:
            for player in row:
                if player:
                    player.draw(background)

    def check_for_clicks(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for row in self.field:
                for chess_square in row:
                    chess_square.select(event, self.player_field)
            #print(self.player_field)

    def _setup_player_field(self, background):
        for y in range(0, 8):
            row = []
            for x in range(0, 8):
                row.append(None)
            self.player_field.append(row)
        self._spawn_bauern(background)

    def _spawn_bauern(self, background):
        x, y = 0, 100
        black = self.player_field[1]
        white = self.player_field[6]
        for position in range(0, 8):
            black[position] = Bauer(x, y, 100, 100, background, 'black', 'sprites/Bauer-Black.png')
            x += 100
        y = 600
        x = 0
        for position in range(0, 8):
            white[position] = Bauer(x, y, 100, 100, background, 'white', 'sprites/Bauer-Weiß.png')
            x += 100
        print(self.player_field)

    def color(self):
        if self.black_or_white == 0:
            self.black_or_white = 1
            return self.black
        else:
            self.black_or_white = 0
            return self.white

    def color_swap(self):
        if self.black_or_white == 0:
            self.black_or_white = 1
        else:
            self.black_or_white = 0

    def update_player_field(self, index, value):
        x, y = index
        self.player_field[y][x] = value
