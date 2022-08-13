import pygame

from .constants import BUTTON_TOP_COLOR, BUTTON_BOTTOM_COLOR, MENU_HEIGHT, MENU_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE_COLOR

class Button:
	def __init__(self, menu_surface:pygame.Surface, text:str, width:int, height:int, offset_x:int, offset_y:int, elevation:float, pressed:bool, button_group:list, func:any, func_arg:any=None, top_color:any=BUTTON_TOP_COLOR, bottom_color:any=BUTTON_BOTTOM_COLOR) -> None:
		self.menu_surface = menu_surface
		self.menu_center_x = MENU_WIDTH / 2
		self.menu_center_y = MENU_HEIGHT / 2
		self.button_group = button_group
		self.func = func
		self.func_arg = func_arg

		# Core attributes 
		self.pressed = pressed
		self.elevation = elevation
		self.dynamic_elevation = elevation
		self.font = pygame.font.Font(None, 30)
		self.original_y = self.menu_center_y + offset_y
		self.original_color = top_color
 
		# Top rectangle 
		self.top_rect = pygame.Rect(0, 0, width, height)
		self.top_rect.center = (self.menu_center_x+offset_x, self.menu_center_y+offset_y)
		self.top_color = self.original_color
 
		# Bottom rectangle 
		self.bottom_rect = pygame.Rect(self.top_rect)
		self.bottom_color = bottom_color

		# Text
		self.text = text
		self.text_surface = self.font.render(text, True, WHITE_COLOR)
		self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

		if not self.button_group:
			self.button_group.append(self)
 
	def update(self) -> None:
		self.check_click()

	def draw(self) -> None:
		# Elevation logic
		self.top_rect.y = self.original_y - self.dynamic_elevation
		self.text_rect.center = self.top_rect.center
 
		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
 
		pygame.draw.rect(self.menu_surface, self.bottom_color, self.bottom_rect, border_radius=12)
		pygame.draw.rect(self.menu_surface, self.top_color, self.top_rect, border_radius=12)
		self.menu_surface.blit(self.text_surface, self.text_rect)
		
 
	def check_click(self) -> None:
		mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
		mouse_pos = (mouse_pos_x-(SCREEN_WIDTH-MENU_WIDTH)/2, mouse_pos_y-(SCREEN_HEIGHT-MENU_HEIGHT)/2)
		if self.top_rect.collidepoint(mouse_pos) or self.pressed:
			if pygame.mouse.get_pressed()[0] or self.pressed:
				for button in self.button_group:
					button.pressed = False
				self.dynamic_elevation = 0
				self.pressed = True
				if self.func_arg:
					self.func(self.func_arg)
				else:
					self.func()
		if not self.pressed:
			self.dynamic_elevation = self.elevation
