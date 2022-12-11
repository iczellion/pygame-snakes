from dataclasses import dataclass, field
from typing import List

from snake import TSnake, Orientation

class TGame:

    @staticmethod
    def initialize(game_name: str, grid_size_pixels: int, grid_num_squares: int):

        # initialize game
        tgame = TGame()
        tgame.score = 0
        tgame.game_name = "Snake"
        tgame.tsnake = None

        bvalid = tgame.__validate_size_square_fits(grid_size_pixels, grid_num_squares)
        if not bvalid:
            raise ValueError("grid_size_pixels modulo grid_num_squares doesn't equate zero.  Fatal error.")

        tgame.grid_size_pixels = grid_size_pixels
        tgame.grid_num_squares = grid_num_squares

        return tgame

    def create_snake(self):
        size_of_one_square = self.grid_size_pixels / self.grid_num_squares
        default_orientation = Orientation.RIGHT
        self.tsnake = TSnake(size_of_one_square, default_orientation)

    def __validate_size_square_fits(self, grid_size_pixels: int, grid_num_squares: int):
        if grid_size_pixels % grid_num_squares > 0:
            return False
        
        return True
    
    def coord_is_out_of_bound(self, coords: tuple):
        if  (coords[0] >= self.grid_size_pixels or
            coords[0] < 0 or
            coords[1] >= self.grid_size_pixels or
            coords[1] < 0):
            return True
        return False
    
    def set_score(self, score: int):
        self.score = score