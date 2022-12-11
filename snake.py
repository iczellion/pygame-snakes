from dataclasses import dataclass
from enum import Enum

class Orientation(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class TSnake:

    def __init__(self, scale_factor: int, head_orientation: Orientation):
        self.scale_factor = scale_factor
        self.head_orientation = head_orientation
        self.length: int = 1
        self.head_x = scale_factor + scale_factor
        self.head_y = 0
        self.snake_parts = []
        self.is_alive = True

        self.add_snake_part((0, 0))
        self.add_snake_part((scale_factor, 0))
    
    def move_snake_head(self, orientation: Orientation):
        orientation_before = self.head_orientation
        self.head_orientation = orientation

        if orientation == Orientation.UP:
            self.head_y = self.head_y - self.scale_factor
        elif orientation == Orientation.RIGHT:
            self.head_x = self.head_x + self.scale_factor
        elif orientation == Orientation.DOWN:
            self.head_y = self.head_y + self.scale_factor
        elif orientation == Orientation.LEFT:
            self.head_x = self.head_x - self.scale_factor
    
    def add_snake_part(self, coords: tuple):
        self.snake_parts.append(coords)
    
    def remove_snake_part(self):
        self.snake_parts.pop(0)
    
    def move_snake(self, orientation: Orientation):
        head_coords_before_x = self.head_x
        head_coords_before_y = self.head_y

        self.move_snake_head(orientation)
        self.remove_snake_part()
        self.add_snake_part((head_coords_before_x, head_coords_before_y))
        