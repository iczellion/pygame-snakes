import pygame

from game import TGame
from snake import TSnake, Orientation

class InputCtrl():

    def __init__(self, tgame):
        self.tgame = tgame
        self.controls_enabled = True

    def set_controls_enabled(self, val: bool):
        self.controls_enabled = val

    def change_gamestate_on_keydown(self):
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.tgame.is_terminated = True
            if event.type == pygame.KEYDOWN and self.controls_enabled:
                if event.key == pygame.K_LEFT and self.tgame.tsnake.head_orientation != Orientation.RIGHT:
                    self.tgame.tsnake.head_orientation = Orientation.LEFT
                elif event.key == pygame.K_RIGHT and self.tgame.tsnake.head_orientation != Orientation.LEFT:
                    self.tgame.tsnake.head_orientation = Orientation.RIGHT
                elif event.key == pygame.K_UP and self.tgame.tsnake.head_orientation != Orientation.DOWN:
                    self.tgame.tsnake.head_orientation = Orientation.UP
                elif event.key == pygame.K_DOWN and self.tgame.tsnake.head_orientation != Orientation.UP:
                    self.tgame.tsnake.head_orientation = Orientation.DOWN