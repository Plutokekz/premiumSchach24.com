from src.helper.HelperFunktions import *


class Board:

    def __init__(self):
        self.field = []
        self.init_empty_field()
        self.coord_white, self.coord_black = [], []

    def init_empty_field(self):
        self.field = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(Empty(x, y))
            self.field.append(row)

    def setup(self):
        self._spawn('white')
        self._spawn('black')
        self._update_coords()

    def _spawn(self, team):
        for x, y in spawn_position_pawn(team):
            self.field[y][x] = Pawn(x, y, team)
        for x, y in spawn_position_rock(team):
            self.field[y][x] = Rock(x, y, team)
        for x, y in spawn_position_knight(team):
            self.field[y][x] = Knight(x, y, team)
        for x, y in spawn_position_bishop(team):
            self.field[y][x] = Bishop(x, y, team)
        x, y = spawn_position_king(team)
        self.field[y][x] = King(x, y, team)
        x, y = spawn_position_queen(team)
        self.field[y][x] = Queen(x, y, team)

    def _update_coords(self):
        self.coord_black, self.coord_white = [], []
        for row in self.field:
            for piece in row:
                if piece:
                    if piece.team == 'black':
                        self.coord_black.append((piece.x, piece.y))
                    elif piece.team == 'white':
                        self.coord_white.append((piece.x, piece.y))

    def update(self):
        self._update_coords()

    def select(self, x, y):
        chess_piece = self.field[y][x]
        if chess_piece:
            return chess_piece
        return None

    def move(self, piece, to_piece):
        if piece.team == 'Empty':
            print('can not move Empty')
            return
        possible_moves = piece.possible_moves(white=self.coord_white, black=self.coord_black)
        x_to, y_to = to_piece.x, to_piece.y
        print(piece)
        if (x_to, y_to) in possible_moves.keys():
            if to_piece.team in possible_moves[(x_to, y_to)]:
                self.field[y_to][x_to] = piece
                self.field[piece.y][piece.x] = Empty(piece.x, piece.y)
                piece.x, piece.y = x_to, y_to
                piece.is_first_move = False
                self.update()
            else:
                print(f'It must be {possible_moves[(x_to, y_to)]} and not {to_piece.team} ')
                return
        else:
            print(f'({to_piece.x}, {to_piece.y}) is not a possible move')
            return

    def __repr__(self):
        return f"{self.field[0]}\n{self.field[1]}\n{self.field[2]}\n{self.field[3]}\n{self.field[4]}\n{self.field[5]}"\
               f"\n{self.field[6]}\n{self.field[7]}"


class Piece:

    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.is_first_move = True
        self.enemy = self._get_enemy()

    def _get_enemy(self):
        if self.team == 'black':
            return 'white'
        elif self.team == 'white':
            return 'black'
        return None


class Empty(Piece):

    def __init__(self, x, y, team='Empty'):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"Empty at X: {self.x} Y: {self.y}"


class Pawn(Piece):

    def __init__(self, x, y, team):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"{self.team} Pawn on X: {self.x} Y: {self.y}"

    def possible_moves(self, **kwargs):
        moves = {}
        if self.team == 'white':
            y = '+1'
            y2 = '+2'
        else:
            y = '-1'
            y2 = '-2'
        if self.is_first_move:
            moves[self.x, self.y + int(y2)] = ['Empty']
        for coord, type in {(self.x, self.y + int(y)): ['Empty'], (self.x + 1, self.y + int(y)): [self.enemy],
                            (self.x - 1, self.y + int(y)): [self.enemy]}.items():
            if 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7:
                moves[coord] = type
        return moves


class King(Piece):

    def __init__(self, x, y, team):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"{self.team} King at X: {self.x} Y: {self.y}"


class Queen(Piece):

    def __init__(self, x, y, team):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"{self.team} Queen at X: {self.x} Y: {self.y}"


class Rock(Piece):

    def __init__(self, x, y, team):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"{self.team} Rock at X: {self.x} Y: {self.y}"

    def possible_moves(self, **kwargs):
        if self.team == 'white':
            ally = kwargs['white']
            enemy = kwargs['black']
        else:
            ally = kwargs['black']
            enemy = kwargs['white']
        allowed_moves = {}
        x = self.x
        for y in reversed(range(0, self.y)):
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        for y in range(self.y+1, 8):
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        y = self.y
        for x in reversed(range(0, self.x)):
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        for x in range(self.x + 1, 8):
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        return allowed_moves


class Knight(Piece):

    def __init__(self, x, y, team):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"{self.team} Knight at X: {self.x} Y: {self.y}"

    def possible_moves(self, **kwargs):
        e = self.enemy
        moves = {}
        for coord, _type in {(self.x - 1, self.y + 2): ['Empty', e], (self.x - 2, self.y + 1): ['Empty', e],
                             (self.x + 2, self.y + 1): ['Empty', e], (self.x + 1, self.y + 2): ['Empty', e],
                             (self.x - 1, self.y - 2): ['Empty', e], (self.x - 2, self.y - 1): ['Empty', e],
                             (self.x + 2, self.y - 1): ['Empty', e], (self.x + 1, self.y - 2): ['Empty', e]}.items():
            if 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7:
                moves[coord] = _type
        return moves


class Bishop(Piece):

    def __init__(self, x, y, team):
        Piece.__init__(self, x, y, team)

    def __repr__(self):
        return f"{self.team} Bishop at X: {self.x} Y: {self.y}"

    def possible_moves(self, **kwargs):
        white_coord = kwargs['white']
        black_coord = kwargs['black']
        return self._move_calculator(white_coord, black_coord)

    def _move_calculator(self, white_coord, black_coord):
        if self.team == 'white':
            ally = white_coord
            enemy = black_coord
        else:
            ally = black_coord
            enemy = white_coord
        allowed_moves = {}
        x = self.x
        for y in reversed(range(0, self.y)):
            x -= 1
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        x = self.x
        for y in range(self.y+1, 8):
            x += 1
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        x = self.x
        for y in reversed(range(0, self.y)):
            x += 1
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        x = self.x
        for y in range(self.y + 1, 8):
            x -= 1
            if (x, y) in ally:
                break
            elif (x, y) in enemy:
                allowed_moves[(x, y)] = [self.enemy]
                break
            allowed_moves[(x, y)] = ['Empty']
        moves = {}
        for coord, _type in allowed_moves.items():
            if 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7:
                moves[coord] = _type
        return moves
