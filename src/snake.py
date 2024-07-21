from dataclasses import dataclass
from enum import Enum

class Orientation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class TSnake:

    def __init__(self, head_orientation: Orientation):
        self.head_orientation = head_orientation
        self.length: int = 1
        self.head_x = 2
        self.head_y = 0
        self.snake_parts = []
        self.is_alive = True

        self.add_snake_part((0, 0))
        self.add_snake_part((1, 0))
    
    def move_snake_head(self, orientation: Orientation):
        orientation_before = self.head_orientation
        self.head_orientation = orientation

        if orientation == Orientation.UP:
            self.head_y = self.head_y - 1
        elif orientation == Orientation.RIGHT:
            self.head_x = self.head_x + 1
        elif orientation == Orientation.DOWN:
            self.head_y = self.head_y + 1
        elif orientation == Orientation.LEFT:
            self.head_x = self.head_x - 1
    
    def add_snake_part(self, coords: tuple):
        self.snake_parts.append(coords)
    
    def remove_snake_part(self):
        self.snake_parts.pop(0)
    
    def grow_snake(self):
        tail_part = self.snake_parts[len(self.snake_parts) - 1]
        self.add_snake_part((tail_part[0], tail_part[1]))
    
    def move_snake(self, orientation: Orientation):
        head_coords_before_x = self.head_x
        head_coords_before_y = self.head_y

        self.move_snake_head(orientation)
        self.remove_snake_part()
        self.add_snake_part((head_coords_before_x, head_coords_before_y))
    
    def set_alive(self, is_alive: bool):
        self.is_alive = is_alive