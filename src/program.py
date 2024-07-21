import argparse
from enum import Enum

import pygame

from game import TGame
from inputctrl import InputCtrl
from renderer import Renderer
from snake import TSnake, Orientation

class Gamemode(Enum):
    INTERACTIVE = 1
    TRAIN = 2
    AI = 3

def parse_commandline_args() -> str:

    opts = None

    main_parser = argparse.ArgumentParser(add_help=True)
    main_parser.add_argument('--debug', default=False, required=False, action='store_true', dest="debug", help='Set debug flag')
    subparsers = main_parser.add_subparsers(title="service", dest="service_commands")

    interactive_parser = subparsers.add_parser("int", help="Runs snake in interactive mode", add_help=True)
    interactive_parser.set_defaults(mode=Gamemode.INTERACTIVE)

    train_parser = subparsers.add_parser("train", help="Runs snake in auto-training mode", add_help=True)
    train_parser.set_defaults(mode=Gamemode.TRAIN)

    ai_parser = subparsers.add_parser("ai", help="Runs snake in AI mode", add_help=True)
    ai_parser.set_defaults(mode=Gamemode.AI)

    args = main_parser.parse_args()

    if(args.service_commands is None):
        main_parser.print_help()
    else:
        pass
    
    return args.mode

def run(mode: Gamemode):

    tgame = TGame.initialize(game_name="Snake", grid_size_pixels=600, grid_num_squares=20)
    tgame.reset()
    inputctrl = InputCtrl(tgame)

    # Disable reacting to keyboard keydown events
    if mode != Gamemode.INTERACTIVE:
        inputctrl.set_controls_enabled(False)

    pygame.init()
    pygame.display.set_caption(tgame.game_name)
    
    screen = pygame.display.set_mode((tgame.grid_size_pixels, tgame.grid_size_pixels))
    renderer = Renderer(screen)
      
    clock = pygame.time.Clock()

    # main loop
    while not tgame.is_terminated:

        if tgame.tsnake.is_alive == False:
            tgame.reset()

        renderer.render_all(tgame, debug=False)

        # Change game state based on keydown event
        inputctrl.change_gamestate_on_keydown()

        tgame.tsnake.move_snake(tgame.tsnake.head_orientation)

        if(tgame.is_snake_colliding_with_apple()):
            tgame.tsnake.grow_snake()
            tgame.create_apple()

        # Check if snake is out of bounds
        # If it is, it means we are dead and should restart
        if tgame.coord_is_out_of_bound((tgame.tsnake.head_x, tgame.tsnake.head_y)):
            tgame.tsnake.set_alive(False)
            tgame.set_score(0)

        #pygame.display.update()
        pygame.display.flip()

        clock.tick(10)
    
    pygame.quit()
    quit()

if __name__=="__main__":
    gamemode = parse_commandline_args()
    run(gamemode)