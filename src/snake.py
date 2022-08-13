import pygame
from pygame.math import Vector2

from src.constants import BLACK_COLOR, CELL_SIZE, WHITE_COLOR

class Snake:
    def __init__(self, surface:pygame.Surface, color:tuple, cell_number:int) -> None:
        self.cell_number = cell_number
        self.body = [Vector2(self.cell_number//2, self.cell_number//2), Vector2((self.cell_number//2)-1, self.cell_number//2), Vector2((self.cell_number//2)-2, self.cell_number//2)]
        self.direction = Vector2(1, 0)
        self.discarded_bodypart = None
        self.color = color
        self.surface = surface
    
    def draw(self) -> None:
        for i, pos in enumerate(self.body):
            if i == 0:
                self.draw_head(pos, self.body[i+1])
            elif i == len(self.body)-1:
                self.draw_tail(pos, self.body[i-1])
            else:
                prev_pos, next_pos = self.body[i+1], self.body[i-1]
                if (prev_pos.x == next_pos.x) or (prev_pos.y == next_pos.y):
                    self.draw_body(pos)
                else:
                    self.draw_corner(pos, prev_pos, next_pos)

    def move(self) -> None:
        temp_body = self.body[:-1]
        self.discarded_bodypart = self.body[-1]
        temp_body.insert(0, temp_body[0]+self.direction)
        self.body = temp_body[:]
    
    def grow(self) -> None:
        self.body.append(self.discarded_bodypart)
    
    def draw_head(self, pos:Vector2, prev_pos:Vector2) -> None:
        actual_x = pos.x * CELL_SIZE
        actual_y = pos.y * CELL_SIZE
        center = (actual_x+(CELL_SIZE//2), actual_y+(CELL_SIZE//2))
        pupil_offset = CELL_SIZE // 13
        if pos.x-prev_pos.x == 1:
            # Facing right
            rect = pygame.Rect(actual_x, actual_y, CELL_SIZE//2, CELL_SIZE)
            left_eye_center = (actual_x+(CELL_SIZE//2), actual_y+(CELL_SIZE//4))
            right_eye_center = (actual_x+(CELL_SIZE//2), actual_y+CELL_SIZE-(CELL_SIZE//4))
            left_pupil_center = (actual_x+(CELL_SIZE//2)+pupil_offset, actual_y+(CELL_SIZE//4))
            right_pupil_center = (actual_x+(CELL_SIZE//2)+pupil_offset, actual_y+CELL_SIZE-(CELL_SIZE//4))
        elif pos.x-prev_pos.x == -1:
            # Facing left
            rect = pygame.Rect(actual_x+(CELL_SIZE//2), actual_y, CELL_SIZE//2, CELL_SIZE)
            left_eye_center = (actual_x+(CELL_SIZE//2), actual_y+(CELL_SIZE//4))
            right_eye_center = (actual_x+(CELL_SIZE//2), actual_y+CELL_SIZE-(CELL_SIZE//4))
            left_pupil_center = (actual_x+(CELL_SIZE//2)-pupil_offset, actual_y+(CELL_SIZE//4))
            right_pupil_center = (actual_x+(CELL_SIZE//2)-pupil_offset, actual_y+CELL_SIZE-(CELL_SIZE//4))
        elif pos.y - prev_pos.y == 1:
            # Facing down
            rect = pygame.Rect(actual_x, actual_y, CELL_SIZE, CELL_SIZE//2)
            left_eye_center = (actual_x+(CELL_SIZE//4), actual_y+(CELL_SIZE//2))
            right_eye_center = (actual_x+CELL_SIZE-(CELL_SIZE//4), actual_y+(CELL_SIZE//2))
            left_pupil_center = (actual_x+(CELL_SIZE//4), actual_y+(CELL_SIZE//2)+pupil_offset)
            right_pupil_center = (actual_x+CELL_SIZE-(CELL_SIZE//4), actual_y+(CELL_SIZE//2)+pupil_offset)
        elif pos.y - prev_pos.y == -1:
            # Facing up
            rect = pygame.Rect(actual_x, actual_y+(CELL_SIZE//2), CELL_SIZE, CELL_SIZE//2)
            left_eye_center = (actual_x+(CELL_SIZE//4), actual_y+(CELL_SIZE//2))
            right_eye_center = (actual_x+CELL_SIZE-(CELL_SIZE//4), actual_y+(CELL_SIZE//2))
            left_pupil_center = (actual_x+(CELL_SIZE//4), actual_y+(CELL_SIZE//2)-pupil_offset)
            right_pupil_center = (actual_x+CELL_SIZE-(CELL_SIZE//4), actual_y+(CELL_SIZE//2)-pupil_offset)
        # Draw head
        pygame.draw.rect(self.surface, self.color, rect)
        pygame.draw.circle(self.surface, self.color, center, CELL_SIZE//2)
        # Draw eyes
        pygame.draw.circle(self.surface, WHITE_COLOR, left_eye_center, CELL_SIZE//8)
        pygame.draw.circle(self.surface, WHITE_COLOR, right_eye_center, CELL_SIZE//8)
        # Draw pupils
        pygame.draw.circle(self.surface, BLACK_COLOR, left_pupil_center, CELL_SIZE//12)
        pygame.draw.circle(self.surface, BLACK_COLOR, right_pupil_center, CELL_SIZE//12)

    def draw_tail(self, pos:Vector2, next_pos:Vector2) -> None:
        actual_x = pos.x * CELL_SIZE
        actual_y = pos.y * CELL_SIZE
        if pos.x-next_pos.x == 1:
            rect = pygame.Rect(actual_x, actual_y, CELL_SIZE//2, CELL_SIZE)
        elif pos.x-next_pos.x == -1:
            rect = pygame.Rect(actual_x+(CELL_SIZE//2), actual_y, CELL_SIZE//2, CELL_SIZE)
        elif pos.y-next_pos.y == 1:
            rect = pygame.Rect(actual_x, actual_y, CELL_SIZE, CELL_SIZE//2)
        elif pos.y-next_pos.y == -1:
            rect = pygame.Rect(actual_x, actual_y+(CELL_SIZE//2), CELL_SIZE, CELL_SIZE//2)
        pygame.draw.rect(self.surface, self.color, rect)
        center = (actual_x+(CELL_SIZE//2), actual_y+(CELL_SIZE//2))
        pygame.draw.circle(self.surface, self.color, center, CELL_SIZE//2)

    def draw_corner(self, pos:Vector2, prev_pos:Vector2, next_pos:Vector2) -> None:
        actual_x = pos.x * CELL_SIZE
        actual_y = pos.y * CELL_SIZE
        if ((prev_pos.x < pos.x) and (next_pos.y > pos.y)) or ((next_pos.x < pos.x) and (prev_pos.y > pos.y)):
            # Top right
            center = (actual_x, actual_y+CELL_SIZE)
            draw_top_right = True
            draw_top_left = False
            draw_bottom_left = False
            draw_bottom_right = False
        elif ((prev_pos.x < pos.x) and (next_pos.y < pos.y)) or ((next_pos.x < pos.x) and (prev_pos.y < pos.y)):
            # Bottom right
            center = (actual_x, actual_y)
            draw_top_right = False
            draw_top_left = False
            draw_bottom_left = False
            draw_bottom_right = True
        elif ((prev_pos.x > pos.x) and (next_pos.y > pos.y)) or ((next_pos.x > pos.x) and (prev_pos.y > pos.y)):
            # Top left
            center = (actual_x+CELL_SIZE, actual_y+CELL_SIZE)
            draw_top_right = False
            draw_top_left = True
            draw_bottom_left = False
            draw_bottom_right = False
        elif ((prev_pos.x > pos.x) and (next_pos.y < pos.y)) or ((next_pos.x > pos.x) and (prev_pos.y < pos.y)):
            # Bottom left
            center = (actual_x+CELL_SIZE, actual_y)
            draw_top_right = False
            draw_top_left = False
            draw_bottom_left = True
            draw_bottom_right = False
        pygame.draw.circle(self.surface, self.color, center, CELL_SIZE, 0, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)

    def draw_body(self, pos:Vector2) -> None:
        rect = pygame.Rect(pos.x*CELL_SIZE, pos.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.surface, self.color, rect)
