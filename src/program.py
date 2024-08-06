import argparse
from enum import Enum

import pygame

from game import TGame
from inputctrl import InputCtrl
from renderer import Renderer
from snake import TSnake, Orientation
from envs.snake_env import SnakeEnv

class Gamemode(Enum):
    INTERACTIVE = 1
    TRAIN = 2
    AI = 3

def parse_commandline_args() -> tuple:

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
    
    return args.mode, args.debug

def run(mode: Gamemode, debug: bool):

    if mode == Gamemode.INTERACTIVE:
        tgame = TGame.initialize(game_name="Snake", grid_size_pixels=600, grid_num_squares=20, framerate=15, inputs_enabled=True, rendering_enabled=True, debug=debug)

    if mode == Gamemode.AI:
        env = SnakeEnv(game_name="Snake", grid_size_pixels=600, grid_num_squares=20, fov_distance=5)

    quit()

if __name__=="__main__":
    gamemode, debug = parse_commandline_args()
    run(gamemode, debug)