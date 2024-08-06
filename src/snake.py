from dataclasses import dataclass
from enum import Enum

class Orientation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    NONE = 4

class TSnake:

    def __init__(self, head_orientation: Orientation):
        self.head_orientation = head_orientation
        self.orientation_before = head_orientation
        self.initial_length: int = 3
        self.snake_parts = []
        self.is_alive = True

        for i in range(0, self.initial_length - 1):
            self.add_snake_part((i, 0))
        
        self.head_x = self.initial_length - 1
        self.head_y = 0

    def move_snake_head(self, orientation: Orientation):

        if self.orientation_before == Orientation.UP and orientation != Orientation.DOWN:
            self.head_y = self.head_y - 1
        elif self.orientation_before == Orientation.RIGHT and orientation != Orientation.LEFT:
            self.head_x = self.head_x + 1
        elif self.orientation_before == Orientation.DOWN and orientation != Orientation.UP:
            self.head_y = self.head_y + 1
        elif self.orientation_before == Orientation.LEFT and orientation != Orientation.RIGHT:
            self.head_x = self.head_x - 1
        else:
            return False
        
        self.orientation_before = self.head_orientation
        self.head_orientation = orientation
        return True
        
    
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

        snake_movable = self.move_snake_head(orientation)
        if snake_movable:
            self.remove_snake_part()
            self.add_snake_part((head_coords_before_x, head_coords_before_y))
    
    def set_alive(self, is_alive: bool):
        self.is_alive = is_alive