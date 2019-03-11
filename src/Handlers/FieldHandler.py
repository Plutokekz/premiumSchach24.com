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
        self.selection_queue = []
        self.current_player = 'black'

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
            self.background_field.append(row)

    def _spawn_chess_pieces(self, team):
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
                pygame.draw.rect(background, Green, rect, 2)

    def _draw_chess_pieces(self, background):
        for row in self.field:
            for player in row:
                if player.team != 'Empty':
                    player.draw(background)

    def _light_available_moves(self, selection):
        moves = self.allowed_moves(selection)
        rects_to_light = []
        if moves:
            for x, y in moves.keys():
                rects_to_light.append(pygame.Rect(x*100, y*100, 100, 100))
        return rects_to_light

    def _handle_selection(self, x, y):
        rects_to_light = []
        selection = self.select(x, y)

        """Testing"""
        if selection.team == 'black':
            lighten = self.all_allowed_moves_black
        else:
            lighten = self.all_allowed_moves_white
        for piece, moves in lighten.items():
            for x, y in moves:
                rects_to_light.append(pygame.Rect(x * 100, y * 100, 100, 100))
        """Testing"""

        if len(self.selection_queue) == 0:
            if selection.team != self.current_player:
                print(f'You are: {self.current_player} not {selection.team}')
                return
            if selection.team == 'Empty':
                return
        self.selection_queue.append(selection)
        if len(self.selection_queue) == 1:
            self.chess_squares_to_lighten = rects_to_light#self._light_available_moves(selection)
        if len(self.selection_queue) == 2:
            if self.move(self.selection_queue[0], self.selection_queue[1]) is True:
                self._player_swap()
            self.selection_queue[:] = []
            self.chess_squares_to_lighten[:] = []

    def _player_swap(self):
        if self.current_player == 'black':
            self.current_player = 'white'
        else:
            self.current_player = 'black'

    def setup(self):
        self._spawn_chess_background_field()
        self._init_empty_field()
        self._spawn_chess_pieces('black')
        self._spawn_chess_pieces('white')
        self.update()

    def draw(self, background):
        self._draw_background(background)
        self._draw_chess_pieces(background)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for row in self.background_field:
                for chess_square in row:
                    coords = chess_square.select(event)
                    if coords:
                        x, y = coords[0], coords[1]
                        print(f'Clicked Chess Square: X: {x}, Y: {y}')
                        self._handle_selection(x, y)
