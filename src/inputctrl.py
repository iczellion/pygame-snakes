from __future__ import annotations

import pygame

from snake import TSnake, Orientation

class InputCtrl():

    def __init__(self, tgame: TGame):
        self.tgame = tgame
        self.controls_enabled = True

    def set_controls_enabled(self, val: bool):
        self.controls_enabled = val

    def change_gamestate_input_events(self):
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.tgame.set_terminated(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return Orientation.LEFT
                elif event.key == pygame.K_RIGHT:
                    return Orientation.RIGHT
                elif event.key == pygame.K_UP:
                    return Orientation.UP
                elif event.key == pygame.K_DOWN:
                    return Orientation.DOWN
        
        return Orientation.NONE