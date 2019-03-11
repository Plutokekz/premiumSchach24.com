from src.helpers.SpawnPositions import *


class Board:

    def __init__(self):
        self.field = []
        self._init_empty_field()
        self.coord_white, self.coord_black = [], []
        self.pieces_white, self.pieces_black = [], []
        self.all_allowed_moves_white, self.all_allowed_moves_black = {}, {}

    def _init_empty_field(self):
        self.field = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(Empty(x, y))
            self.field.append(row)

    def _update_all_allowed_moves(self):
        self.all_allowed_moves_white.clear()
        self.all_allowed_moves_black.clear()
        for enemy in self.pieces_white:
            positions = self.allowed_moves(enemy)
            self.all_allowed_moves_white[enemy] = positions.keys()
        for enemy in self.pieces_black:
            positions = self.allowed_moves(enemy)
            self.all_allowed_moves_black[enemy] = positions.keys()

    def _update_coords(self):
        self.coord_black, self.coord_white = [], []
        self.pieces_white, self.pieces_black = [], []
        for row in self.field:
            for piece in row:
                if piece:
                    if piece.team == 'black':
                        self.coord_black.append((piece.x, piece.y))
                        self.pieces_black.append(piece)
                    elif piece.team == 'white':
                        self.coord_white.append((piece.x, piece.y))
                        self.pieces_white.append(piece)

    def _check_for_game_over(self, current_team):
        if current_team == 'black':
            enemies = self.pieces_white
            moves = self.all_allowed_moves_black
        else:
            enemies = self.pieces_white
            moves = self.all_allowed_moves_white
        for enemy in enemies:
            if type(enemy) == King:
                if enemy.possible_moves(enemies=moves) is None:
                    print(f'Winner {current_team}')
                    exit()

    def update(self):
        self._update_coords()
        self._update_all_allowed_moves()

    def select(self, x, y):
        chess_piece = self.field[y][x]
        print(f'Selection from Matrix: {chess_piece}')
        if chess_piece:
            return chess_piece
        return None

    def _move(self, piece, x, y):
        target = self.field[y][x]
        self.field[y][x] = piece
        self.update()
        return {piece.name: (piece.x, piece.y), target.name: (x, y)}

    def allowed_moves(self, piece):
        if piece.team == 'Empty':
            print('Empty field can not move')
            return
        if piece.team == 'white':
            all_enemies = self.all_allowed_moves_black
        else:
            all_enemies = self.all_allowed_moves_white
        possible_moves = piece.possible_moves(white=self.coord_white, black=self.coord_black, enemies=all_enemies)
        real_possible_moves = possible_moves.copy()
        for x, y in possible_moves.keys():
            if self.field[y][x].team in possible_moves[(x, y)]:
                pass
            else:
                del real_possible_moves[(x, y)]
        return real_possible_moves

    def _rochhade(self, piece, to_piece, enemies):
        if to_piece.x == 0:
            x_king = 2
            x_rock = 3
            coords = [(1, piece.y), (2, piece.y), (3, piece.y)]
        elif to_piece.x == 7:
            x_king = 6
            x_rock = 5
            coords = [(5, piece.y), (6, piece.y)]
        for x, y in coords:
            if self.select(x, y).team != 'Empty':
                return None
        #print('Hallo wo bist du ? ', piece.check_coord((piece.y, x_king), enemies))
        #if piece.check_coord((piece.y, x_king), enemies) is None:
        self._move(piece, x_king, piece.y)
        self._move(to_piece, x_rock, to_piece.y)
        self._move(Empty(piece.x, piece.y), piece.x, piece.y)
        self._move(Empty(to_piece.x, to_piece.y), to_piece.x, to_piece.y)
        piece.x, to_piece.x = x_king, x_rock
        #for graphic
        piece.x_pos, to_piece.x_pos = int(x_king * 100), int(x_rock * 100)
        piece.is_first_move = False
        to_piece.is_first_move = False
        return True

    def move(self, piece, to_piece):
        if piece.team == 'Empty':
            print('can not move Empty')
            return None
        if str(piece) == 'King':
            print('King KING KING KING')
            if piece.team == 'white':
                all_enemies = self.all_allowed_moves_black
            else:
                all_enemies = self.all_allowed_moves_white
            possible_moves = piece.possible_moves(white=self.coord_white, black=self.coord_black, enemies=all_enemies)
            print(to_piece.team, piece.team, str(to_piece), 'Rock', to_piece.is_first_move)
            if to_piece.team == piece.team and str(to_piece) == 'Rock' and to_piece.is_first_move:
                print(all_enemies)
                if self._rochhade(piece, to_piece, all_enemies):
                    self._check_for_game_over(piece.team)
                    print('Played Rochade')
                    return True
        else:
            possible_moves = piece.possible_moves(white=self.coord_white, black=self.coord_black)
        x_to, y_to = to_piece.x, to_piece.y
        print(f'From: {piece}, To: {to_piece}, Possible moves From: {possible_moves}')
        if (x_to, y_to) in possible_moves.keys():
            if to_piece.team in possible_moves[(x_to, y_to)]:
                self._move(piece, x_to, y_to)
                self._move(Empty(piece.x, piece.y), piece.x, piece.y)
                piece.x, piece.y = x_to, y_to
                #for graphic
                piece.x_pos, piece.y_pos = int(x_to*100), int(y_to*100)
                piece.is_first_move = False
                self.update()
                self._check_for_game_over(piece.team)
                return True
            else:
                print(f'It must be {possible_moves[(x_to, y_to)]} and not {to_piece.team} ')
                return None
        else:
            print(f'({to_piece.x}, {to_piece.y}) is not a possible move')
            return None

    def __repr__(self):
        return f"{self.field[0]}\n{self.field[1]}\n{self.field[2]}\n{self.field[3]}\n{self.field[4]}\n{self.field[5]}"\
               f"\n{self.field[6]}\n{self.field[7]}"


class Piece:

    def __init__(self, x, y, team, name, value):
        self.x = x
        self.y = y
        self.team = team
        self.is_first_move = True
        self.name = team + name
        self.enemy = self._get_enemy()
        self.value = value

    def _get_enemy(self):
        if self.team == 'black':
            return 'white'
        elif self.team == 'white':
            return 'black'
        return None


class Empty(Piece):

    def __init__(self, x, y, team='Empty', value=0):
        Piece.__init__(self, x, y, team, '-empty', value)

    def __repr__(self):
        return f"Empty at X: {self.x} Y: {self.y}"


class Pawn(Piece):

    def __init__(self, x, y, team, value=1):
        Piece.__init__(self, x, y, team, 'pawn', value)

    def __repr__(self):
        return f"{self.team} Pawn on X: {self.x} Y: {self.y}"

    def possible_moves(self, **kwargs):
        moves = {}
        if self.team == 'white':
            y = '+1'
            y2 = '+2'
            ally = kwargs['white']
            enemy = kwargs['black']
        else:
            y = '-1'
            y2 = '-2'
            ally = kwargs['black']
            enemy = kwargs['white']
        x = self.x
        if self.is_first_move and (self.x, self.y + int(y)) not in enemy and (self.x, self.y + int(y)) not in ally:
            moves[self.x, self.y + int(y2)] = ['Empty']
        for coord, _type in {(self.x, self.y + int(y)): ['Empty'], (self.x + 1, self.y + int(y)): [self.enemy],
                            (self.x - 1, self.y + int(y)): [self.enemy]}.items():
            if 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7:
                moves[coord] = _type
        return moves


class King(Piece):

    def __init__(self, x, y, team, value=0):
        Piece.__init__(self, x, y, team, '-king', value)

    def __repr__(self):
        return f"{self.team} King at X: {self.x} Y: {self.y}"

    def possible_moves(self, **kwargs):
        enemies = kwargs['enemies']
        print(f'Test: {enemies}')
        moves = {}
        for coord, _type in {(self.x - 1, self.y - 1): ['Enemy', 'Empty'], (self.x, self.y - 1): ['Enemy', 'Empty'],
                             (self.x + 1, self.y - 1): ['Enemy', 'Empty'], (self.x - 1, self.y): ['Enemy', 'Empty'],
                             (self.x + 1, self.y): ['Enemy', 'Empty'], (self.x - 1, self.y + 1): ['Enemy', 'Empty'],
                             (self.x, self.y + 1): ['Enemy', 'Empty'], (self.x + 1, self.y + 1): ['Enemy', 'Empty'],
                             }.items():
            if 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7:
                moves[coord] = _type
        return self._matt(enemies, moves)

    def _matt(self, all_allowed_enemie_moves, moves):
        copy_moves = moves.copy()
        for coord, _type in copy_moves.items():
            if _type.name == 'Pawn':
                pass
            if self.check_coord(coord, all_allowed_enemie_moves):
                del moves[coord]
        if moves:
            return moves
        return None

    def matt(self, all_allowed_enemies_moves):
        for _type, moves in all_allowed_enemies_moves.items():
            if (self.x, self.y) in moves:
                return _type, moves
        return None


    @staticmethod
    def check_coord(coord, enemies):
        print(coord)
        for _ , moves in enemies.items():
            if coord in moves:
                return True
        return None


class Queen(Piece):

    def __init__(self, x, y, team, value=9):
        Piece.__init__(self, x, y, team, '-queen', value)

    def __repr__(self):
        return f"{self.team} Queen at X: {self.x} Y: {self.y}"

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
        for y in range(self.y + 1, 8):
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
        for y in range(self.y + 1, 8):
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


class Rock(Piece):

    def __init__(self, x, y, team, value=5):
        Piece.__init__(self, x, y, team, '-rock', value)

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

    def __init__(self, x, y, team, value=3):
        Piece.__init__(self, x, y, team, '-knight', value)

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

    def __init__(self, x, y, team, value=3):
        Piece.__init__(self, x, y, team, '-bishop', value)

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
