import pygame
from pygame.math import Vector2

from src.constants import BACKGROUND_COLOR, CELL_SIZE, GRASS_COLOR, SCREEN_HEIGHT, SCREEN_UPDATE, SCREEN_WIDTH, SCORE_COLOR
from src.fruit import Fruit
from src.snake import Snake

class GameController:
	def __init__(self, main_surface:pygame.Surface, game_over:any, snake_color:tuple, cell_number:int) -> None:
		self.game_over = game_over
		self.cell_number = cell_number
		
		if cell_number == 20:
			self.score_factor = 1
		elif cell_number == 15:
			self.score_factor = 2
		else:
			self.score_factor = 5

		self.main_surface = main_surface
		self.game_surface = pygame.Surface((cell_number*CELL_SIZE, cell_number*CELL_SIZE))
		self.game_surface.convert_alpha()
		self.main_center = self.game_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

		self.score_font = pygame.font.Font('font/roboto/Roboto-Regular.ttf', 25)
		self.snake_color = snake_color
		self.staged_direction = None
		self.score = '0'

		self.new_game()

	def update(self, event:pygame.event.Event) -> None:
		if event.type == SCREEN_UPDATE:
			if self.staged_direction:
				self.snake.direction, self.staged_direction = self.staged_direction, None
			self.snake.move()
			self.check_game_over()
			self.check_fruit_eaten()
		if event.type == pygame.KEYDOWN:
			up_pressed = (event.key == pygame.K_UP or event.key == pygame.K_w)
			down_pressed = (event.key == pygame.K_DOWN or event.key == pygame.K_s)
			left_pressed = (event.key == pygame.K_LEFT or event.key == pygame.K_a)
			right_pressed = (event.key == pygame.K_RIGHT or event.key == pygame.K_d)
			if up_pressed and (self.snake.direction.y != 1):
				self.staged_direction = Vector2(0, -1)
			if down_pressed and (self.snake.direction.y != -1):
				self.staged_direction = Vector2(0, 1)
			if left_pressed and (self.snake.direction.x != 1):
				self.staged_direction = Vector2(-1, 0)
			if right_pressed and (self.snake.direction.x != -1):
				self.staged_direction = Vector2(1, 0)
    
	def draw(self) -> None:
		self.draw_grass()
		self.snake.draw()
		self.fruit.draw()
		self.draw_score()

		self.main_surface.blit(self.game_surface, self.main_center)
    
	def check_fruit_eaten(self) -> None:
		if self.fruit.pos == self.snake.body[0]:
			self.snake.grow()
			self.score = str((len(self.snake.body)-3)*self.score_factor)
			self.fruit.randomize()
			self.check_invalid_fruit()
    
	def check_game_over(self) -> None:
		if not ((0 <= self.snake.body[0].x < self.cell_number) and (0 <= self.snake.body[0].y < self.cell_number)):
			self.game_over()
        
		for segment in self.snake.body[1:]:
			if segment == self.snake.body[0]:
				self.game_over()

	def draw_score(self) -> None:
		score_surface = self.score_font.render(self.score, True, SCORE_COLOR)
		score_pos = (CELL_SIZE*(self.cell_number-2), CELL_SIZE*(self.cell_number-1))
		score_rect = score_surface.get_rect(center = score_pos)

		self.game_surface.blit(score_surface, score_rect)

	def new_game(self) -> None:
		self.snake = Snake(self.game_surface, self.snake_color, self.cell_number)
		self.fruit = Fruit(self.game_surface, self.cell_number)
		self.check_invalid_fruit()
    
	def check_invalid_fruit(self) -> None:
		while self.fruit.pos in self.snake.body:
			self.fruit.randomize()

	def draw_grass(self) -> None:
		for col in range(self.cell_number):
			for row in range(self.cell_number):
				if (col%2 == 0 and row%2 != 0) or (col%2 != 0 and row%2 == 0):
					color = GRASS_COLOR
				else:
					color = BACKGROUND_COLOR
				border_bottom_left_radius = 0
				border_bottom_right_radius = 0
				border_top_left_radius = 0
				border_top_right_radius = 0
				if self.cell_number != 20:
					if (col == 0) and (row == 0):
						border_top_left_radius = 8
					elif (col == self.cell_number-1) and (row == 0):
						border_top_right_radius = 8
					elif (col == 0) and (row == self.cell_number-1):
						border_bottom_left_radius = 8
					elif (col == self.cell_number-1) and (row == self.cell_number-1):
						border_bottom_right_radius = 8
				rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
				pygame.draw.rect(self.game_surface, color, rect, CELL_SIZE, border_bottom_left_radius=border_bottom_left_radius, border_bottom_right_radius=border_bottom_right_radius, border_top_left_radius=border_top_left_radius, border_top_right_radius=border_top_right_radius)
