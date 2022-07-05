import pygame
from src.colors import white, black, board1_color, board2_color, snake_head_color, snake_body_color, apple_color
import random as rnd
import sqlite3

class Game:
    def __init__(self, cell_width: int, cell_height: int, board_start: int, board_end: int, number_of_cells_x: int, number_of_cells_y: int, snake: object, has_started = False) -> None:
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.board_start = board_start
        self.board_end = board_end
        self.number_of_cells_x = number_of_cells_x
        self.number_of_cells_y = number_of_cells_y

        self.has_started = has_started
        self.game_over = False

        self.snake = snake
        self.apple_x = -1
        self.apple_y = -1
        self.apple_eaten = True

        self.score = 0
        with sqlite3.connect('src/score.db') as connection:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS highscore(id INTEGER PRIMARY KEY, score INTEGER)')
            cursor.execute('SELECT score FROM highscore')
            data = cursor.fetchall()
            if (len(data) != 0):
                self.highscore = data[0][0]
            else:
                self.highscore = 0

    def calculate_x_on_board(self, x: int) -> int:
        if not 0 <= x < self.number_of_cells_x:
            self.game_over = True
        return x * self.cell_width + self.cell_width
    
    def calculate_y_on_board(self, y: int) -> int:
        if not 0 <= y < self.number_of_cells_y:
            self.game_over = True
        return y * self.cell_height + self.cell_height

    def draw_board(self, screen: pygame.Surface) -> list:
        screen.fill(white)

        # Draw cells
        for y in range(self.board_start, self.board_end + 1, self.cell_height):
            for x in range(self.board_start, self.board_end + 1, self.cell_width):
                if (x + y) % (self.board_start * 2) == 0:
                    pygame.draw.rect(screen, board1_color, [x, y, self.cell_width, self.cell_height])
                else:
                    pygame.draw.rect(screen, board2_color, [x, y, self.cell_width, self.cell_height])
        
        # Draw snake
        pygame.draw.rect(screen, snake_head_color, [self.calculate_x_on_board(self.snake.head.x), self.calculate_y_on_board(self.snake.head.y), self.cell_width, self.cell_height])
        for body_part in self.snake.body:
            pygame.draw.rect(screen, snake_body_color, [self.calculate_x_on_board(body_part.x), self.calculate_y_on_board(body_part.y), self.cell_width, self.cell_height])

        # Draw apple
        if self.apple_eaten:
            possible_apples = []
            for y in range(self.number_of_cells_y):
                for x in range(self.number_of_cells_x):
                    if self.snake.head.x != x or self.snake.head.y != y:
                        appendable = True
                        for body_part in self.snake.body:
                            if body_part.x == x and body_part.y == y:
                                appendable = False
                        if appendable:
                            possible_apples.append((x, y))
            apple_index = rnd.randint(0, len(possible_apples) - 1)
            self.apple_x = possible_apples[apple_index][0]
            self.apple_y = possible_apples[apple_index][1]
        apple_position_x = self.calculate_x_on_board(self.apple_x)
        apple_position_y = self.calculate_y_on_board(self.apple_y)
        pygame.draw.circle(screen, apple_color, (apple_position_x + self.cell_width // 2 - self.cell_width // 20, apple_position_y + self.cell_height // 2 + self.cell_height // 20), self.cell_width / 3)
        pygame.draw.polygon(screen, snake_body_color, [(apple_position_x + self.cell_width // 2 + self.cell_width // 15, apple_position_y + self.cell_height // 2 - self.cell_height // 10), (apple_position_x + self.cell_width // 2 + self.cell_width // 5, apple_position_y + self.cell_height // 2 - self.cell_height // 6), (apple_position_x + self.cell_width // 2 + self.cell_width // 5, apple_position_y + self.cell_height // 2 - self.cell_height // 4)])

        # Draw score
        font = pygame.font.Font('freesansbold.ttf', 28)
        score_text = font.render(f'Score: {self.score}', True, black)
        score_text_rectangle = score_text.get_rect()
        score_text_rectangle.center = (int(self.cell_width * 3.5), self.board_end + int(self.cell_height * 2.5))
        screen.blit(score_text, score_text_rectangle)

        # Draw highscore
        highscore_text = font.render(f'Highscore: {self.highscore}', True, black)
        highscore_text_rectangle = highscore_text.get_rect()
        highscore_text_rectangle.center = (int(self.cell_width * 3.5), self.board_end + int(self.cell_height * 3.5))
        screen.blit(highscore_text, highscore_text_rectangle)

        # Draw game over
        if self.game_over:
            self.draw_game_over(screen)
        
        # Draw start screen
        if not self.has_started:
            start_text = font.render('Press SPACE to start', True, black, snake_body_color)
            start_text_rectangle = start_text.get_rect()
            start_text_rectangle.center = (int(self.cell_width * 12), self.board_end + int(self.cell_height * 3))
            screen.blit(start_text, start_text_rectangle)

    def draw_game_over(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 28)
        game_over_text = font.render('Game over!', True, black, apple_color)
        game_over_text_rectangle = game_over_text.get_rect()
        game_over_text_rectangle.center = (int(self.cell_width * 12), self.board_end + int(self.cell_height * 2.5))
        screen.blit(game_over_text, game_over_text_rectangle)

        restart_text = font.render('Press SPACE to restart', True, black, apple_color)
        restart_text_rectangle = restart_text.get_rect()
        restart_text_rectangle.center = (int(self.cell_width * 12), self.board_end + int(self.cell_height * 3.5))
        screen.blit(restart_text, restart_text_rectangle)

    def tick(self, screen):
        self.apple_eaten = self.snake.move(self.apple_x, self.apple_y)
        self.score = self.snake.get_length() - 1
        if self.score > self.highscore:
            with sqlite3.connect('src/score.db') as connection:
                cursor = connection.cursor()

                # Delete old highscore if exists
                cursor.execute('SELECT score FROM highscore')
                data = cursor.fetchall()
                if (len(data) != 0):
                    cursor.execute('DELETE from highscore WHERE id = 1')

                # Add new highscore
                cursor.execute(f'''INSERT INTO highscore VALUES
                  (:id, :score)''', {'id': 1, 'score': self.score})
                
                # Fetch new highscore
                cursor.execute('SELECT score FROM highscore')
                data = cursor.fetchall()
                self.highscore = data[0][0]
        if self.snake.dead:
            self.draw_game_over(screen)
            pygame.display.update()
            self.game_over = True
            