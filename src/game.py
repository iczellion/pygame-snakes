from dataclasses import dataclass, field
from typing import List
import random

import pygame

from snake import TSnake, Orientation
from renderer import Renderer
from inputctrl import InputCtrl

class TGame:

    @staticmethod
    def initialize(game_name: str, grid_size_pixels: int, grid_num_squares: int, framerate: int, inputs_enabled: bool, rendering_enabled: bool, debug: bool):

        # initialize game
        tgame = TGame()
        tgame.debug = debug
        tgame.set_score(0)
        tgame.set_terminated(False)
        tgame.game_name = game_name
        tgame.tsnake = None
        tgame.apple_coords = None
        tgame.fov_distance = 5
        tgame.framerate = framerate

        tgame.inputctrl = InputCtrl(tgame)

        # Disable reacting to keyboard keydown events
        if not inputs_enabled:
            tgame.inputctrl.set_controls_enabled(False)

        bvalid = tgame.__validate_size_square_fits(grid_size_pixels, grid_num_squares)
        if not bvalid:
            raise ValueError("grid_size_pixels modulo grid_num_squares doesn't equate zero.  Fatal error.")

        tgame.grid_size_pixels = grid_size_pixels
        tgame.grid_num_squares = grid_num_squares

        pygame.init()

        if rendering_enabled:
            tgame.renderer = Renderer(tgame)

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

    def is_snake_colliding_with_itself(self):
        for part in self.tsnake.snake_parts:
            if part[0] == self.tsnake.head_x and part[1] == self.tsnake.head_y:
                return True
        return False

    def reset(self):
        self.create_snake()
        self.create_apple()
        self.set_score(0)
        self.set_terminated(False)
    
    def set_terminated(self, is_terminated: bool):
        self.is_terminated = is_terminated
    
    def close(self):
        pygame.quit()
    
    def perform_action(self, orientation: Orientation):
        # Prevent the snake from reversing directly onto itself
        if  (orientation == Orientation.UP and self.tsnake.head_orientation == Orientation.DOWN) or \
            (orientation == Orientation.DOWN and self.tsnake.head_orientation == Orientation.UP) or \
            (orientation == Orientation.LEFT and self.tsnake.head_orientation == Orientation.RIGHT) or \
            (orientation == Orientation.RIGHT and self.tsnake.head_orientation == Orientation.LEFT):
                orientation = self.tsnake.head_orientation  # Maintain current direction

        # Calculate where the head will be after moving
        new_head_x = self.tsnake.head_x
        new_head_y = self.tsnake.head_y
    
        if orientation == Orientation.UP:
            new_head_y -= 1
        elif orientation == Orientation.RIGHT:
            new_head_x += 1
        elif orientation == Orientation.DOWN:
            new_head_y += 1
        elif orientation == Orientation.LEFT:
            new_head_x -= 1
        
        # Check if the next move would be out of bounds
        if self.coord_is_out_of_bound((new_head_x, new_head_y)):
            if self.debug:
                print("Snake out of bound")

            self.tsnake.set_alive(False)
            self.set_score(0)
            return False

        # Check if the next move would collide with snake body
        if (new_head_x, new_head_y) in self.tsnake.snake_parts:
            if self.debug:
                print("Snake collided with itself")

            self.tsnake.set_alive(False)
            self.set_score(0)
            return False
        
        # If we get here, the move is safe, so execute it
        self.tsnake.move_snake(orientation)

        if(self.is_snake_colliding_with_apple()):
            if self.debug:
                print("Snake eats an apple")

            self.tsnake.grow_snake()
            self.create_apple()
            self.set_score(self.score + 1)

        return True

    def start_game_loop(self):
        renderer = self.renderer
        inputctrl = self.inputctrl

        # Start clock, used for game loop
        clock = pygame.time.Clock()

        # main loop
        while not self.is_terminated:

            if self.tsnake.is_alive == False:
                self.reset()

            future_orientation = self.tsnake.head_orientation

            # Change game state base on events event
            input_orientation = inputctrl.change_gamestate_input_events()
            if inputctrl.controls_enabled:
                if input_orientation != Orientation.NONE:
                    future_orientation = input_orientation
            
            action_possible = self.perform_action(future_orientation)

            renderer.render_all()

            clock.tick(self.framerate)
        
        self.close()