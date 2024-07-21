from dataclasses import dataclass, field
from typing import List
import random

from snake import TSnake, Orientation

class TGame:

    @staticmethod
    def initialize(game_name: str, grid_size_pixels: int, grid_num_squares: int):

        # initialize game
        tgame = TGame()
        tgame.score = 0
        tgame.is_terminated = False
        tgame.game_name = "Snake"
        tgame.tsnake = None
        tgame.apple_coords = None
        tgame.fov_distance = 5

        bvalid = tgame.__validate_size_square_fits(grid_size_pixels, grid_num_squares)
        if not bvalid:
            raise ValueError("grid_size_pixels modulo grid_num_squares doesn't equate zero.  Fatal error.")

        tgame.grid_size_pixels = grid_size_pixels
        tgame.grid_num_squares = grid_num_squares

        return tgame

    def create_snake(self):
        default_orientation = Orientation.RIGHT
        self.tsnake = TSnake(default_orientation)
    
    def create_apple(self):
        random_x = random.randrange(0, self.grid_num_squares)
        random_y = random.randrange(0, self.grid_num_squares)

        self.apple_coords = (random_x, random_y)

    def __validate_size_square_fits(self, grid_size_pixels: int, grid_num_squares: int):
        if grid_size_pixels % grid_num_squares > 0:
            return False
        
        return True
    
    def coord_is_out_of_bound(self, coords: tuple):
        if  (coords[0] >= self.grid_num_squares or
            coords[0] < 0 or
            coords[1] >= self.grid_num_squares or
            coords[1] < 0):
            return True
        return False
    
    def set_score(self, score: int):
        self.score = score
    
    def is_snake_colliding_with_apple(self):
        if self.tsnake.head_x == self.apple_coords[0] and self.tsnake.head_y == self.apple_coords[1]:
            return True
        return False

    def reset(self):
        self.create_snake()
        self.create_apple()
        self.set_score(0)
        self.is_terminated = False