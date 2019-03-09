import pygame
from src.helpers.SelectionQueue import SelectionQueue
from src.Objects.GameObjects import Pawn as gPawn, Queen as gQueen, King as gKing, Bishop as gBishop, \
    Knight as gKnight, Rock as gRock

selection_queue = SelectionQueue()


class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, team, img_path):
        pygame.sprite.Sprite.__init__(self)
        object_image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(object_image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.rectangle_draging = False
        self.offset_x = 0
        self.offset_y = 0
        self.team = team
        self.highlight_image = None
        self.first_move = True

    @staticmethod
    def check_position(field, x, y):
        player = field[y][x]
        if player:
            return player.team
        return None

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

    def highlight(self):
        self.highlight_image = self.image.copy()
        self.image.fill((0, 100, 0) + (0,), None, pygame.BLEND_RGBA_ADD)

    def un_highlight(self):
        self.image = self.highlight_image

    def select(self, event, field):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                current_x_index, current_y_index = self.x_pos / 100, self.y_pos / 100
                selection_queue.add(current_x_index, current_y_index, field)

    def get_index(self):
        return int(self.x_pos / 100), int(self.y_pos / 100)


class Pawn(GameObject, gPawn):

    def __init__(self, x, y, width, height, team, img_path):
        GameObject.__init__(self, x, y, width, height, team, img_path)
        gPawn.__init__(self, x, y, team)


class Queen(GameObject, gQueen):

    def __init__(self, x, y, width, height, team, img_path):
        GameObject.__init__(self, x, y, width, height, team, img_path)
        gQueen.__init__(self, x, y, team)


class King(GameObject, gKing):

    def __init__(self, x, y, width, height, team, img_path):
        GameObject.__init__(self, x, y, width, height, team, img_path)
        gKing.__init__(self, x, y, team)


class Bishop(GameObject, gBishop):

    def __init__(self, x, y, width, height, team, img_path):
        GameObject.__init__(self, x, y, width, height, team, img_path)
        gBishop.__init__(self, x, y, team)


class Knight(GameObject, gKnight):

    def __init__(self, x, y, width, height, team, img_path):
        GameObject.__init__(self, x, y, width, height, team, img_path)
        gKnight.__init__(self, x, y, team)


class Rock(GameObject, gRock):

    def __init__(self, x, y, width, height, team, img_path):
        GameObject.__init__(self, x, y, width, height, team, img_path)
        gRock.__init__(self, x, y, team)


class ChessSquare(pygame.sprite.Sprite):

    def __init__(self, x, y, color, width, height, thickness):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.thickness = thickness
        self.rect = pygame.Rect(x, y, width, height)

    def select(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                current_x_index, current_y_index = self.x / 100, self.y / 100
                return current_x_index, current_y_index
