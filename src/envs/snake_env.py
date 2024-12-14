import numpy as np

import gymnasium as gym
from gymnasium import spaces

from snake import Orientation, TSnake
from game import TGame

class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, game_name: str, grid_size_pixels: int, grid_num_squares: int, framerate: int, inputs_enabled: bool, rendering_enabled:bool, debug=False):
        """
        Initialize the Snake environment.
        """

        self.reward_move = -0.01
        self.reward_collision = -10
        self.reward_apple = 20
        self.reward_timeout = -1
        self.reward_surviving = 0

        self.steps_count = 0
        self.steps_max = 1000

        self.action_space = spaces.Discrete(4) # "Up", "Right", "Down", "Left"

        # Update observation space to include multiple frames
        self.observation_space = spaces.Box(
            low=0, # 0 = empty space/wall, 1 = snake part, 2 = snake head, 3 = apple
            high=3,
            shape=(grid_num_squares * grid_num_squares + 6, ), # +2 for apple direction, +4 for current direction
            dtype=np.float32
        )

        self.tgame = TGame.initialize(game_name, grid_size_pixels, grid_num_squares, framerate, inputs_enabled, rendering_enabled, debug)

    def render(self):
        self.tgame.inputctrl.change_gamestate_input_events()

        self.tgame.renderer.render_all()

    def step(self, action):
        self.steps_count += 1
        previous_score = self.tgame.score
        action_possible = self.tgame.perform_action(Orientation(action))

        terminated = not self.tgame.tsnake.is_alive
        truncated = self.steps_count >= self.steps_max

        reward = 0
        if terminated:
            reward = self.reward_collision
        elif previous_score != self.tgame.score:
            reward = self.reward_apple
        elif not action_possible:
            reward = self.reward_collision
        else:
            reward = self.reward_move + self.reward_surviving
        
        observation = self._get_observation()

        # Create info dict for debugging
        info = {
            "score": self.tgame.score,
            "steps": self.steps_count
        }
        
        return observation, reward, terminated, truncated, info
        
    def _get_observation(self):
        # Create empty grid filled with zeros
        current_grid = np.zeros((self.tgame.grid_num_squares, self.tgame.grid_num_squares), dtype=np.int32)

        # Add snake body parts (value 1)
        for part in self.tgame.tsnake.snake_parts:
            current_grid[part[1]][part[0]] = 1

        # Add snake head (value 2)
        current_grid[self.tgame.tsnake.head_y][self.tgame.tsnake.head_x] = 2

        # Add apple (value 3)
        current_grid[self.tgame.apple_coords[1]][self.tgame.apple_coords[0]] = 3

        # Add direction to apple
        apple_direction = np.array([
            self.tgame.apple_coords[0] - self.tgame.tsnake.head_x,
            self.tgame.apple_coords[1] - self.tgame.tsnake.head_y,
        ])

        # Add current direction
        current_direction = np.zeros(4)  # one-hot encoding of direction
        current_direction[self.tgame.tsnake.head_orientation.value] = 1

        obs = np.concatenate([
            current_grid.flatten(),
            apple_direction,
            current_direction
        ])

        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Reset the RNG if provided
        self.tgame.reset()
        self.steps_count = 0

        observation = self._get_observation()
        info = {"score": 0, "steps": 0}

        return observation, info

    
    def close(self):
        self.tgame.set_terminated(True)
        self.tgame.close()
        super().close()