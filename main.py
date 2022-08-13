import sys
import pygame

from src.constants import BACKGROUND_COLOR, BLACK_COLOR, CELL_SIZE, GRASS_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH
from src.menu_controller import MenuController
from src.game_controller import GameController

class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Snake')
        pygame.mouse.set_cursor(pygame.cursors.tri_left)

        self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.menu_controller = MenuController(self.main_surface)
        self.game_controller = None

        self.clock = pygame.time.Clock()
    
    def start_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.update(event)
            
            self.draw()

            pygame.display.update()

            self.clock.tick(60)

    def update(self, event:pygame.event.Event) -> None:
        if not self.game_controller is None:
            self.menu_controller.current_score = self.game_controller.score
            self.game_controller.update(event)
        elif self.menu_controller.started_game:
            self.game_controller = GameController(self.main_surface, self.game_over, self.menu_controller.snake_color, self.menu_controller.cell_number)
        else:
            self.menu_controller.update()

    def draw(self) -> None:
        if not self.game_controller is None:
            self.main_surface.fill(BLACK_COLOR)
            self.game_controller.draw()
        else:
            self.main_surface.fill(BACKGROUND_COLOR)
            self.draw_grass()
            self.menu_controller.draw()
    
    def draw_grass(self) -> None:
        for col in range(20):
            for row in range(20):
                if (col%2 == 0 and row%2 != 0) or (col%2 != 0 and row%2 == 0):
                    rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.main_surface, GRASS_COLOR, rect, CELL_SIZE)
    
    def game_over(self) -> None:
        self.game_controller = None
        self.menu_controller.start_button.pressed = False
        self.menu_controller.started_game = False
        pygame.mouse.set_visible(True)

if __name__ == '__main__':
    main = Main()
    main.start_loop()
