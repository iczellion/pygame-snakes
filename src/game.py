from dataclasses import dataclass, field
from typing import List
import random

import pygame

from snake import TSnake, Orientation

class TGame:

    @staticmethod
    def initialize(game_name: str, grid_size_pixels: int, grid_num_squares: int, framerate: int, inputs_enabled: bool, rendering_enabled: bool, debug: bool):

        from renderer import Renderer

        # initialize game
        tgame = TGame()
        tgame.score = 0
        tgame.is_terminated = False
        tgame.game_name = game_name
        tgame.tsnake = None
        tgame.apple_coords = None
        tgame.fov_distance = 5

        # Enable reacting to keyboard keydown events
        if inputs_enabled:
            from inputctrl import InputCtrl

            tgame.inputctrl = InputCtrl(tgame)
            tgame.inputctrl.set_controls_enabled(True)

        bvalid = tgame.__validate_size_square_fits(grid_size_pixels, grid_num_squares)
        if not bvalid:
            raise ValueError("grid_size_pixels modulo grid_num_squares doesn't equate zero.  Fatal error.")

        tgame.grid_size_pixels = grid_size_pixels
        tgame.grid_num_squares = grid_num_squares

        pygame.init()

        if rendering_enabled:
            pygame.display.set_caption(game_name)
            tgame.renderer = Renderer(grid_size_pixels, grid_num_squares)

        tgame.reset()

        tgame.start_game_loop(framerate=framerate, debug=debug)

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

    def start_game_loop(self, framerate: int, debug:bool):
        renderer = self.renderer
        inputctrl = self.inputctrl

        # Start clock, used for game loop
        clock = pygame.time.Clock()

        # main loop
        while not self.is_terminated:

            if self.tsnake.is_alive == False:
                self.reset()

            renderer.render_all(self, debug=debug)

            # Change game state based on keydown event
            inputctrl.change_gamestate_on_keydown()

            self.tsnake.move_snake(self.tsnake.head_orientation)

            if(self.is_snake_colliding_with_apple()):
                self.tsnake.grow_snake()
                self.create_apple()

            # Check if snake is out of bounds
            # If it is, it means we are dead and should restart
            if self.coord_is_out_of_bound((self.tsnake.head_x, self.tsnake.head_y)):
                self.tsnake.set_alive(False)
                self.set_score(0)

            #pygame.display.update()
            pygame.display.flip()

            clock.tick(framerate)
        
        pygame.quit()