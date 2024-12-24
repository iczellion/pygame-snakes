import argparse
from datetime import datetime
from enum import Enum
import os

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
    ai_parser.add_argument('--checkpoint', type=str, required=False,
                          help='Path to model checkpoint file')

    args = main_parser.parse_args()

    if(args.service_commands is None):
        main_parser.print_help()
    else:
        pass
    
    return args.mode, args.debug, getattr(args, 'checkpoint', None)

def get_last_directory_asc(base_path: str) -> str:
    """Returns path to the directory with the name in the last alphabetical order"""
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Directory {base_path} not found")
        
    # Get all subdirectories
    all_dirs = [d for d in os.listdir(base_path) 
                  if os.path.isdir(os.path.join(base_path, d))]
    
    if not all_dirs:
        raise FileNotFoundError("No directories found")
        
    # Sort by timestamp (newest first)
    latest_dir = sorted(all_dirs, reverse=True)[0]
        
    return latest_dir

def run(mode: Gamemode, debug: bool = False, checkpoint_path: str = None):
    game_name: str = "Snake"
    grid_size_pixels: int = 600
    grid_num_squares: int = 20
    scratch_dir: str = "./.tmp/"
    model_checkpoints_dir: str = "model_checkpoints"
    training_run_prefix = datetime.now().strftime("%Y%m%d_%H%M")

    if mode == Gamemode.INTERACTIVE:
        framerate: int = 10
        tgame = TGame.initialize(game_name, grid_size_pixels, grid_num_squares, framerate, inputs_enabled=True, rendering_enabled=True, debug=debug)
        tgame.reset()
        tgame.start_game_loop()
    elif mode == Gamemode.AI:
        from ai_controller import AIController

        training_run_prefix = None
        if checkpoint_path:
            training_run_prefix = checkpoint_path
        else:
            training_run_prefix = get_last_directory_asc(os.path.join(scratch_dir, model_checkpoints_dir))

        ai_controller = AIController(
            game_name=game_name,
            grid_size_pixels=grid_size_pixels,
            grid_num_squares=grid_num_squares,
            framerate=15,
            scratch_dir=scratch_dir,
            model_checkpoints_dir=model_checkpoints_dir,
            training_run_prefix=training_run_prefix,
            inputs_enabled=False,
            rendering_enabled=True,
            debug=debug
        )
        ai_controller.run()
    elif mode == Gamemode.TRAIN:
        from ai_controller import AIController
        ai_controller = AIController(
            game_name=game_name,
            grid_size_pixels=grid_size_pixels,
            grid_num_squares=grid_num_squares,
            framerate=0,
            scratch_dir=scratch_dir,
            model_checkpoints_dir=model_checkpoints_dir,
            training_run_prefix=training_run_prefix,
            inputs_enabled=False,
            rendering_enabled=False,
            debug=debug
        )
        ai_controller.train()

    quit()

if __name__=="__main__":
    gamemode, debug, checkpoint_path = parse_commandline_args()
    run(gamemode, debug, checkpoint_path)