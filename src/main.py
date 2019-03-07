import pygame
from src.Handlers.FieldHandler import FieldHandler
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Chess'
WITHE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


class Game:

    def __init__(self, back_ground_color, screen_wight, screen_height, title):
        self.back_ground_color = back_ground_color
        self.height = screen_height
        self.width = screen_wight
        self.title = title
        self.clock = pygame.time.Clock()
        self.TICK_RATE = 60
        self.is_game_over = False

        self.game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.field_handler = FieldHandler()
        self.field_handler.setup_draw(self.game_screen)

    def run(self):
        while not self.is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_over = True
                self.field_handler.check_for_clicks(event)

            pygame.display.update()
            self.field_handler.draw(self.game_screen)
            self.field_handler.draw_board(self.game_screen)
            self.clock.tick(self.TICK_RATE)






pygame.init()

new_game = Game(BLACK_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
new_game.run()

pygame.quit()
quit()
