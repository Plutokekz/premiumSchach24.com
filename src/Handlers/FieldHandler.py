from src.Objects.graphicsObjects import ChessSquare, Pawn, Queen, King, Rock, Bishop, Knight
from src.Objects.GameObjects import Board
from src.helpers.SpawnPositions import *
from src.helpers.Colors import Black, White, Green
import pygame


class ChessBoard(Board):

    def __init__(self, width_height=100):
        super().__init__()
        self.width_height = width_height
        self.background_field = []
        self.black_or_white = 1
        self.chess_squares_to_lighten = []

    def _color(self):
        if self.black_or_white == 0:
            self.black_or_white = 1
            return Black
        else:
            self.black_or_white = 0
            return White

    def _color_swap(self):
        if self.black_or_white == 0:
            self.black_or_white = 1
        else:
            self.black_or_white = 0

    def _spawn_chess_background_field(self):
        x_pos, y_pos = 0, 0
        for y in range(0, 8):
            row = []
            for x in range(0, 8):
                rect = ChessSquare(x_pos, y_pos, self._color(), self.width_height, self.width_height, 0)
                row.append(rect)
                x_pos += 100
            self._color_swap()
            x_pos = 0
            y_pos += 100
            self.field.append(row)

    def _spawn_chess_pieces(self, team):
        self._init_empty_field()
        for x, y in spawn_position_pawn(team):
            self.field[y][x] = Pawn(x*100, y*100, 100, 100, team, f'sprites/Chess_tile_p{team}.png')
        for x, y in spawn_position_rock(team):
            self.field[y][x] = Rock(x*100, y*100, 100, 100, team, f'sprites/Chess_tile_r{team}.png')
        for x, y in spawn_position_knight(team):
            self.field[y][x] = Knight(x*100, y*100, 100, 100, team, f'sprites/Chess_tile_n{team}.png')
        for x, y in spawn_position_bishop(team):
            self.field[y][x] = Bishop(x*100, y*100, 100, 100, team, f'sprites/Chess_tile_b{team}.png')
        x, y = spawn_position_king(team)
        self.field[y][x] = King(x*100, y*100, 100, 100, team, f'sprites/Chess_tile_k{team}.png')
        x, y = spawn_position_queen(team)
        self.field[y][x] = Queen(x*100, y*100, 100, 100, team, f'sprites/Chess_tile_q{team}.png')
        print(f'Spawned Chess Pieces {team}\n{self.field}')

    def _draw_background(self, background):
        for row in self.background_field:
            for rect in row:
                pygame.draw.rect(background, rect.color, rect.rect, rect.thickness)
        if self.chess_squares_to_lighten:
            for rect in self.chess_squares_to_lighten:
                pygame.draw.rect(background, Green, rect, 5)

    def _draw_chess_pieces(self, background):
        for row in self.field:
            for player in row:
                if player:
                    player.draw(background)

    def draw(self, background):
        self._draw_background(background)
        self._draw_chess_pieces(background)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for row in self.background_field:
                for chess_square in row:
                    coords = chess_square.select(event)
                    print(f'Clicked Chess Square: {coords}')
                    if coords:
                        pass


class FieldHandler:

    def _shiny(self, coords):
        x, y = coords
        x, y = int(x), int(y)
        selection = self.board.select(x, y)
        print(selection)
        moves = self.board.allowed_moves(selection)
        rects_to_light = []
        if self.first_selection is not None and self.second_selection is None:
                self.second_selection = selection
        if moves:
            if self.first_selection is None:
                self.first_selection = selection
            for x, y in moves.keys():
                rects_to_light.append(pygame.Rect(x*100, y*100, 100, 100))
        if self.second_selection and self.second_selection:
            self.move()
            return None
        if rects_to_light:
            return rects_to_light

    def _select(self, x, y):
        print(x, y)
        selection = self.player_field[y][x]
        print(f'Bauer: {selection}')
        if selection:
            return selection
        return None

    def _special_rochade_move(self, coord_f, coord_s):
        if coord_s[1] == 0:
            x_king = 2
            x_rock = 3
        elif coord_s[1] == 7:
            x_king = 6
            x_rock = 5
        print(x_king, x_rock)
        king = self._select(coord_f[0], coord_f[1])
        king.x_pos = x_king*100
        rock = self._select(coord_s[0], coord_s[1])
        rock.x_pos = x_rock*100
        self.player_field[coord_f[1]][coord_f[0]] = None
        self.player_field[coord_s[1]][coord_s[0]] = None
        self.player_field[coord_f[1]][x_king] = king
        self.player_field[coord_s[1]][x_rock] = rock

    def move(self):
        x_f, y_f = self.first_selection.x, self.first_selection.y
        x_s, y_s = self.second_selection.x, self.second_selection.y
        moving = self.board.move(self.first_selection, self.second_selection)
        if moving == 'Rochade':
            self._special_rochade_move((x_s, y_s), (x_s, y_s))
        else:
            if type(moving) is bool:
                print('Check first and second selection')
                print(self.first_selection, self.second_selection)
                player = self._select(x_f, y_f)
                if player:
                    self.player_field[y_f][x_f] = None
                    player.x_pos = x_s * 100
                    player.y_pos = y_s * 100
                    self.player_field[y_s][x_s] = player
        self.first_selection, self.second_selection = None, None

    def update_player_field(self, index, value):
        x, y = index
        self.player_field[y][x] = value
