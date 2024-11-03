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
        self.num_stacked_frames = 2
        self.frame_stack = np.zeros((self.num_stacked_frames, grid_num_squares, grid_num_squares), dtype=np.uint8) # Initialize the frame stack

        self.action_space = spaces.Discrete(4) # "Up", "Right", "Down", "Left"

        # Update observation space to include multiple frames
        self.observation_space = spaces.Box(
            low=0, # 0 = empty space/wall, 1 = snake part, 2 = snake head, 3 = apple
            high=3,
            shape=(self.num_stacked_frames, grid_num_squares, grid_num_squares),
            dtype=np.uint8
        )

        self.tgame = TGame.initialize(game_name=game_name, grid_size_pixels=grid_size_pixels, grid_num_squares=grid_num_squares, framerate=15, inputs_enabled=False, rendering_enabled=True, debug=self.debug)

    def render(self):
        self.tgame.inputctrl.change_gamestate_input_events()

        self.tgame.renderer.render_all()

    def step(self, actions):
        self.steps_count += 1
        previous_score = self.tgame.score
        action_possible = self.tgame.perform_action(Orientation(actions))

        terminated = not self.tgame.tsnake.is_alive
        truncated = self.steps_count >= self.steps_max

        reward = 0
        if terminated:
            reward = self.reward_collision
        elif action_possible:
            if previous_score != self.tgame.score:
                reward = self.reward_apple
            elif self.steps_count % 5 == 0:
                reward = self.reward_surviving
            else:
                reward = self.reward_move
        
        observation = self._get_observation()

        # Create info dict for debugging
        info = {
            "score": self.tgame.score,
            "steps": self.steps_count
        }
        
        return observation, reward, terminated, truncated, info
        
    def _get_observation(self):
        # Shift existing frames one position forward in the stack
        if self.num_stacked_frames > 1 and self.steps_count > 1:
            self.frame_stack[1:] = self.frame_stack[:-1]

        # Create empty grid filled with zeros
        current_grid = np.zeros((self.tgame.grid_num_squares, self.tgame.grid_num_squares), dtype=np.uint8)

        # Add snake body parts (value 1)
        for part in self.tgame.tsnake.snake_parts:
            current_grid[part[1]][part[0]] = 1

        # Add snake head (value 2)
        current_grid[self.tgame.tsnake.head_y][self.tgame.tsnake.head_x] = 2

        # Add apple (value 3)
        current_grid[self.tgame.apple_coords[1]][self.tgame.apple_coords[0]] = 3

        # Update the newest frame in the stack
        self.frame_stack[0] = current_grid

        return self.frame_stack

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Reset the RNG if provided
        self.tgame.reset()
        self.steps_count = 0

        # Clear frame stack
        self.frame_stack = np.zeros((self.num_stacked_frames, self.tgame.grid_num_squares, self.tgame.grid_num_squares), dtype=np.uint8)

        observation = self._get_observation()
        info = {"score": 0, "steps": 0}

        return observation, info

    
    def close(self):
        self.tgame.set_terminated(True)
        self.tgame.close()
        super().close()