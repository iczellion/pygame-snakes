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
    game_name: str = "Snake"
    grid_size_pixels: int = 600
    grid_num_squares: int = 20
    model_path: str = "./.tmp/"

    if mode == Gamemode.INTERACTIVE:
        framerate: int = 10
        tgame = TGame.initialize(game_name, grid_size_pixels, grid_num_squares, framerate, inputs_enabled=True, rendering_enabled=True, debug=debug)
        tgame.reset()
        tgame.start_game_loop()
    elif mode == Gamemode.AI:
        from ai_controller import AIController
        ai_controller = AIController(
            game_name=game_name,
            grid_size_pixels=grid_size_pixels,
            grid_num_squares=grid_num_squares,
            framerate=15,  # Faster framerate for AI
            inputs_enabled=False,
            rendering_enabled=True,
            debug=debug,
            scratch_dir=model_path
        )
        ai_controller.run()
    elif mode == Gamemode.TRAIN:
        from ai_controller import AIController
        ai_controller = AIController(
            game_name=game_name,
            grid_size_pixels=grid_size_pixels,
            grid_num_squares=grid_num_squares,
            framerate=20,  # No framerate limit during training
            inputs_enabled=False,
            rendering_enabled=False,  # Disable rendering during training
            debug=debug,
            scratch_dir=model_path
        )
        ai_controller.train()

    quit()

if __name__=="__main__":
    gamemode, debug = parse_commandline_args()
    run(gamemode, debug)