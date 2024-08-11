import numpy as np

import gymnasium as gym
from gymnasium import spaces

from snake import Orientation, TSnake
from game import TGame

class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, game_name="Snake-rl", grid_size_pixels=600, grid_num_squares=20, fov_distance=5):
        """
        Initialize the Snake environment.

        Args:
            grid_size_pixels (int): Size of the grid in pixels.
            grid_num_squares (int): Number of squares in the grid.
            fov_distance (int): Distance (in number of squares) of how far the snake will see.
            num_frames (int): Number of frames to stack in the observation space.
        """
        self.debug = True
        self.reward_move = -1
        self.reward_collision = -1000
        self.reward_apple = 100
        self.reward_timeout = 0
        self.reward_surviving = 5

        self.steps_count = 0
        self.steps_max = 1000
        self.num_stacked_frames = 0
        self.frame_stack = np.zeros((self.num_stacked_frames, fov_distance, fov_distance), dtype=np.uint8) # Initialize the frame stack

        self.action_space = spaces.Discrete(4) # "Up", "Right", "Down", "Left"

        # Update observation space to include multiple frames
        self.observation_space = spaces.Box(
            low=0, # 0 = empty space/wall, 1 = snake part, 2 = snake head, 3 = apple
            high=2,
            shape=(fov_distance, fov_distance, self.num_stacked_frames),
            dtype=np.uint8
        )

        self.tgame = TGame.initialize(game_name=game_name, grid_size_pixels=grid_size_pixels, grid_num_squares=grid_num_squares, framerate=15, inputs_enabled=False, rendering_enabled=True, debug=self.debug)

    def render(self):
        self.tgame.inputctrl.change_gamestate_input_events()

        self.tgame.renderer.render_all()

    def step(self, actions):
        self.step_count += 1
        previous_score = self.tgame.score
        self.tgame.perform_action(Orientation(actions))

        done = self.tgame.tsnake.is_alive
        reward = 0
        
        if not self.tgame.tsnake.is_alive:
            reward = self.reward_collision
        elif previous_score != self.tgame.score:
            reward = self.reward_apple
        elif self.step_count % 5 == 0:
            reward = self.reward_surviving
        else:
            reward = self.reward_move
        
        # Gymnasium v0.26+ returns 5 elements
        # return obs, reward, terminated, truncated, info

    def reset(self):
        self.tgame.reset()
        self.step_count = 0
    
    def close(self):
        self.tgame.set_terminated(True)
        self.tgame.close()
        super().close()