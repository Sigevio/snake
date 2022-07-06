import sys
import pygame
from src.snake import Snake
from src.game import Game

if __name__ == '__main__':
    cell_width = 40
    cell_height = 40
    board_start = 40
    board_end = 600
    number_of_cells_x = 15
    number_of_cells_y = 15

    snake = Snake(number_of_cells_x // 2, 0)
    game = Game(cell_width, cell_height, board_start, board_end, number_of_cells_x, number_of_cells_y, snake)

    pygame.init()
    screen = pygame.display.set_mode((680, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Snake')

    game.draw_board(screen)
    pygame.display.update()

    def main():
        while True:
            can_change_direction = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and can_change_direction:
                    if event.key == pygame.K_LEFT and game.snake.direction != 'right':
                        game.snake.direction = 'left'
                    elif event.key == pygame.K_RIGHT and game.snake.direction != 'left':
                        game.snake.direction = 'right'
                    elif event.key == pygame.K_UP and game.snake.direction != 'down':
                        game.snake.direction = 'up'
                    elif event.key == pygame.K_DOWN and game.snake.direction != 'up':
                        game.snake.direction = 'down'
                    can_change_direction = False
            game.tick(screen)
            if game.game_over:
                break
            game.draw_board(screen)
            pygame.display.update()
            clock.tick(8)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game.has_started:
                    game.has_started = True
                    main()
                else:
                    snake = Snake(number_of_cells_x // 2, 0)
                    game = Game(cell_width, cell_height, board_start, board_end, number_of_cells_x, number_of_cells_y, snake, True)

                    pygame.init()

                    game.draw_board(screen)
                    pygame.display.update()

                    main()
