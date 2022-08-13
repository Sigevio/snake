import pygame

from src.button import Button

from .constants import BLACK_COLOR, DARK_GRAY_COLOR, DARK_GREEN_COLOR, DARK_PINK_COLOR, GRAY_COLOR, GREEN_COLOR, MENU_BOX_COLOR, MENU_HEIGHT, MENU_WIDTH, PINK_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH

class MenuController:
    def __init__(self, main_surface:pygame.Surface) -> None:
        self.main_surface = main_surface
        self.menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.menu_surface = self.menu_surface.convert_alpha()
        self.font = pygame.font.Font('font/roboto/Roboto-Regular.ttf', 40)

        self.highscore_path = 'state/highscore.txt'

        self.current_score = 'N/A'

        self.snake_color_buttons = []
        self.cell_number_buttons = []

        self.main_center = self.menu_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        # Snake color box
        self.box_1 = pygame.Rect(0, 0, 500, 150)
        self.box_1.center = (MENU_WIDTH/2, MENU_HEIGHT/2-215)

        # Snake color text
        self.text_surface_1 = self.font.render('Snake color', True, BLACK_COLOR)
        self.text_rect_1 = self.text_surface_1.get_rect(center=(MENU_WIDTH/2, (MENU_HEIGHT/2)-255))

        # Snake color buttons
        self.snake_color_buttons.append(Button(self.menu_surface, 'Green', 100, 50, -150, -210, 7, True, self.snake_color_buttons, self.set_snake_color, GREEN_COLOR, GREEN_COLOR, DARK_GREEN_COLOR))
        self.snake_color_buttons.append(Button(self.menu_surface, 'Pink', 100, 50, 0, -210, 7, False, self.snake_color_buttons, self.set_snake_color, PINK_COLOR, PINK_COLOR, DARK_PINK_COLOR))
        self.snake_color_buttons.append(Button(self.menu_surface, 'Gray', 100, 50, 150, -210, 7, False, self.snake_color_buttons, self.set_snake_color, GRAY_COLOR, GRAY_COLOR, DARK_GRAY_COLOR))

        # Cell number box
        self.box_2 = pygame.Rect(0, 0, 500, 150)
        self.box_2.center = (MENU_WIDTH/2, (MENU_HEIGHT/2)-40)

        # Cell number text
        self.text_surface_2 = self.font.render('Board size', True, BLACK_COLOR)
        self.text_rect_2 = self.text_surface_2.get_rect(center=(MENU_WIDTH/2, (MENU_HEIGHT/2)-80))

        # Cell number buttons
        self.cell_number_buttons.append(Button(self.menu_surface, '20x20', 100, 50, -150, -35, 7, True, self.cell_number_buttons, self.set_cell_number, 20))
        self.cell_number_buttons.append(Button(self.menu_surface, '15x15', 100, 50, 0, -35, 7, False, self.cell_number_buttons, self.set_cell_number, 15))
        self.cell_number_buttons.append(Button(self.menu_surface, '10x10', 100, 50, 150, -35, 7, False, self.cell_number_buttons, self.set_cell_number, 10))

        # Score & start box
        self.box_3 = pygame.Rect(0, 0, 500, 220)
        self.box_3.center = (MENU_WIDTH/2, (MENU_HEIGHT/2)+170)

        # Start button
        self.start_button = Button(self.menu_surface, 'Start', 200, 50, 0, 210, 7, False, [], self.start_game)

        self.cell_number = 20
        self.snake_color = GREEN_COLOR
        self.started_game = False

    def update(self) -> None:
        for button in self.snake_color_buttons:
            button.update()
        for button in self.cell_number_buttons:
            button.update()
        
        # Update score texts
        self.text_1_surface_3 = self.font.render(f'Score: {self.current_score}', True, BLACK_COLOR)
        self.text_2_surface_3 = self.font.render(f'Highscore: {self.get_highscore()}', True, BLACK_COLOR)
        self.text_1_rect_3 = self.text_1_surface_3.get_rect(center=(MENU_WIDTH/2, (MENU_HEIGHT/2)+100))
        self.text_2_rect_3 = self.text_2_surface_3.get_rect(center=(MENU_WIDTH/2, (MENU_HEIGHT/2)+160))
        
        self.start_button.update()

    def draw(self) -> None:
        pygame.draw.rect(self.menu_surface, MENU_BOX_COLOR, self.box_1, border_radius=8)
        pygame.draw.rect(self.menu_surface, MENU_BOX_COLOR, self.box_2, border_radius=8)
        pygame.draw.rect(self.menu_surface, MENU_BOX_COLOR, self.box_3, border_radius=8)

        self.menu_surface.blit(self.text_surface_1, self.text_rect_1)
        self.menu_surface.blit(self.text_surface_2, self.text_rect_2)
        self.menu_surface.blit(self.text_1_surface_3, self.text_1_rect_3)
        self.menu_surface.blit(self.text_2_surface_3, self.text_2_rect_3)

        for button in self.snake_color_buttons:
            button.draw()
        for button in self.cell_number_buttons:
            button.draw()
        
        self.start_button.draw()

        self.main_surface.blit(self.menu_surface, self.main_center)
    
    def get_highscore(self) -> int:
        open(self.highscore_path, 'a').close()
        with open(self.highscore_path, 'r', encoding='utf-8') as f:
            highscore = f.read()
            if highscore == '':
                highscore = '0'
            if self.current_score == 'N/A':
                score = '0'
            else:
                score = self.current_score
        if int(highscore) < int(score):
            with open(self.highscore_path, 'w', encoding='utf-8') as f:
                f.write(score)
            return score
        return highscore
    
    def set_cell_number(self, value:int) -> None:
        self.cell_number = value
    
    def set_snake_color(self, value:tuple) -> None:
        self.snake_color = value

    def start_game(self) -> None:
        self.started_game = True
        pygame.mouse.set_visible(False)
