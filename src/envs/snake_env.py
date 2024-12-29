from collections import deque

import gymnasium as gym
from gymnasium import spaces
import numpy as np

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
            low=-9999,
            high=9999,
            shape=(43, ),
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
        """
        Returns a 14-dimensional observation vector:

        Index | Feature                      | Description
        ------|------------------------------|-------------------------------------------
        0     | wall_up                      | 1 if there is a wall directly above, else 0
        1     | wall_right                   | 1 if there is a wall directly to the right, else 0
        2     | wall_down                    | 1 if there is a wall directly below, else 0
        3     | wall_left                    | 1 if there is a wall directly to the left, else 0
        4     | snake_up                     | 1 if the snake's body is directly above, else 0
        5     | snake_right                  | 1 if the snake's body is directly to the right, else 0
        6     | snake_down                   | 1 if the snake's body is directly below, else 0
        7     | snake_left                   | 1 if the snake's body is directly to the left, else 0
        8     | delta_x_to_apple             | Horizontal distance to the apple (positive if apple is to the right, negative if to the left)
        9     | delta_y_to_apple             | Vertical distance to the apple (positive if apple is below, negative if above)
        10    | direction_up                 | 1 if the current direction is up, else 0
        11    | direction_right              | 1 if the current direction is right, else 0
        12    | direction_down               | 1 if the current direction is down, else 0
        13    | direction_left               | 1 if the current direction is left, else 0

        Notes:
        - `delta_x_to_apple` and `delta_y_to_apple` represent the relative position of the apple with respect to the snake's head.
        - The direction features (indices 10-13) use one-hot encoding to indicate the snake's current movement direction.
        
        Returns:
            np.ndarray: A 14-dimensional numpy array of type float32 representing the current state observation.
        """
        # Convenience references
        head_x = self.tgame.tsnake.head_x
        head_y = self.tgame.tsnake.head_y
        apple_x, apple_y = self.tgame.apple_coords
        grid_size = self.tgame.grid_num_squares
        snake_body = set(self.tgame.tsnake.snake_parts)  # So membership checks are O(1)

        # Add current direction
        current_direction = np.zeros(4)  # one-hot encoding of direction
        current_direction[self.tgame.tsnake.head_orientation.value] = 1

        # Add direction to apple
        delta_x_to_apple = self.tgame.apple_coords[0] - self.tgame.tsnake.head_x
        delta_y_to_apple = self.tgame.apple_coords[1] - self.tgame.tsnake.head_y

        # Local view (5x5 window centered on the snake's head)
        local_view = np.zeros((5, 5), dtype=np.float32)
        for i in range(5):
            for j in range(5):
                # Convert (i, j) in local window to actual board coords
                board_x = head_x + (j - 2)
                board_y = head_y + (i - 2)

                # Out of bounds => wall
                if board_x < 0 or board_x >= grid_size or board_y < 0 or board_y >= grid_size:
                    local_view[i, j] = 3.0
                else:
                    # Check if it's the snake
                    if (board_x, board_y) in snake_body:
                        local_view[i, j] = 1.0
                    # Check if it's the apple
                    elif (board_x, board_y) == (apple_x, apple_y):
                        local_view[i, j] = 2.0
                    # Otherwise it's empty
                    else:
                        local_view[i, j] = 0.0

        directions = {
            0: (0, -1),   # Up    (dx=0,  dy=-1)
            1: (1, 0),    # Right (dx=1,  dy=0)
            2: (0, 1),    # Down  (dx=0,  dy=1)
            3: (-1, 0)    # Left  (dx=-1, dy=0)
        }

        # Calculate corridor lengths in each direction
        corridor_lengths = np.zeros((4,), dtype=np.float32)
        for d in range(4):
            dx, dy = directions[d]
            steps = 0
            cur_x, cur_y = head_x, head_y

            while True:
                # Move one step in the direction
                cur_x += dx
                cur_y += dy

                # Check boundary
                if cur_x < 0 or cur_x >= grid_size or cur_y < 0 or cur_y >= grid_size:
                    break  # hit a wall
                # Check snake body
                if (cur_x, cur_y) in snake_body:
                    break  # hit the snake's body

                # If it's free, increment corridor length
                steps += 1

            corridor_lengths[d] = steps
        
         # Breadth-First search for distance to apple to avoid snake trapping/boxing itself
        def bfs_distance_and_free_squares(
            start_x, start_y, apple_x, apple_y, snake_body, grid_size
        ):
            """
            Returns:
                (bfs_distance_to_apple, free_squares_reachable)
            where:
            - bfs_distance_to_apple is -1 if apple not reachable from start.
            - free_squares_reachable is the number of empty squares reachable from start.
            """
            # If the start is invalid (outside grid or in snake body), return defaults
            if (
                start_x < 0 or start_x >= grid_size or
                start_y < 0 or start_y >= grid_size or
                (start_x, start_y) in snake_body
            ):
                return -1, 0

            visited = set()
            queue = deque([(start_x, start_y, 0)])
            visited.add((start_x, start_y))

            bfs_distance_to_apple = -1

            while queue:
                x, y, dist = queue.popleft()
                if (x, y) == (apple_x, apple_y):
                    bfs_distance_to_apple = dist
                    # Do NOT break if you still want to explore all reachable squares 
                    # for the free_squares count. 
                    # If you only need BFS distance, you can break here. 
                    # But let's keep exploring for the full free-squares count.

                # Check neighbors
                for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if (
                        0 <= nx < grid_size and
                        0 <= ny < grid_size and
                        (nx, ny) not in snake_body and
                        (nx, ny) not in visited
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))

            free_squares_reachable = len(visited)
            return bfs_distance_to_apple, free_squares_reachable
        
        bfs_features = []
        for action in range(4):
            dx, dy = directions[action]
            next_x = head_x + dx
            next_y = head_y + dy

            distance_to_apple, free_squares = bfs_distance_and_free_squares(
                next_x, next_y, apple_x, apple_y, snake_body, grid_size
            )

            # Add them to a list
            bfs_features.append(distance_to_apple)
            bfs_features.append(free_squares)

        # Now we have 8 BFS features in bfs_features (2 for each direction).
        bfs_features = np.array(bfs_features, dtype=np.float32)

        obs = np.concatenate([
            np.array([delta_x_to_apple, delta_y_to_apple], dtype=np.float32),
            current_direction,
            local_view.flatten(),
            corridor_lengths,
            bfs_features
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