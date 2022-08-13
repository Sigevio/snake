import pygame
from pygame.math import Vector2
import random as rnd

from src.constants import CELL_SIZE, FRUIT_COLOR, FRUIT_SHADOW_COLOR, FRUIT_LEAF_COLOR

class Fruit:
    def __init__(self, surface:pygame.Surface, cell_number:int) -> None:
        self.cell_number = cell_number
        self.randomize()
        self.surface = surface

    def draw(self) -> None:
        actual_x = self.pos.x * CELL_SIZE
        actual_y = self.pos.y * CELL_SIZE
        fruit_center = (actual_x+(CELL_SIZE//2), actual_y+(CELL_SIZE//2))
        leaf_coordinates = [
            (actual_x+(CELL_SIZE//2)+5, actual_y+(CELL_SIZE//2)-5),
            (actual_x+(CELL_SIZE//2)+8, actual_y+(CELL_SIZE//2)-10),
            (actual_x+(CELL_SIZE//2)+9, actual_y+(CELL_SIZE//2)-10)
        ]
        pygame.draw.circle(self.surface, FRUIT_COLOR, fruit_center, CELL_SIZE//3)
        pygame.draw.circle(self.surface, FRUIT_SHADOW_COLOR, fruit_center, CELL_SIZE//3, CELL_SIZE//20, False, False, True, False)
        pygame.draw.polygon(self.surface, FRUIT_LEAF_COLOR, leaf_coordinates)
    
    def randomize(self) -> None:
        self.pos = Vector2(rnd.randint(0, self.cell_number-1), rnd.randint(0, self.cell_number-1))
