import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
import pygame

from envs.snake_env import SnakeEnv

class AIController:
    def __init__(self, game_name: str, grid_size_pixels: int, grid_num_squares: int, framerate: int, inputs_enabled: bool = False, rendering_enabled: bool = False, debug: bool = False, scratch_dir: str = ".tmp"):
        self.game_name = game_name
        self.grid_size_pixels = grid_size_pixels
        self.grid_num_squares = grid_num_squares
        self.framerate = framerate
        self.inputs_enabled = inputs_enabled
        self.rendering_enabled = rendering_enabled
        self.debug = debug
        self.scratch_dir = scratch_dir
        self.model_path = os.path.join(self.scratch_dir, "model_checkpoints")
        self.model_prefix = "snake_ppo_model"

    def __make_env(self, rank):
        """
        Utility function for multiprocessed env.
        """
        def _init():
            env = SnakeEnv(
                game_name=self.game_name,
                grid_size_pixels=self.grid_size_pixels,
                grid_num_squares=self.grid_num_squares,
                framerate=self.framerate,
                inputs_enabled=self.inputs_enabled,
                rendering_enabled=self.rendering_enabled,
                debug=self.debug
            )
            return env
        return _init

    def train(self):
        """Train the snake AI model"""

        # Create 8 environments running in parallel
        num_envs = 8
        env = SubprocVecEnv([self.__make_env(i) for i in range(num_envs)])

        try:
            # Initialize the PPO agent
            model = PPO("MlpPolicy",
                    env,
                    device="cpu",
                    verbose=1, 
                    learning_rate=0.0003,
                    n_steps=2048,
                    batch_size=64,
                    n_epochs=10,
                    tensorboard_log="./.tmp/tensorboard"
            )

            # Create checkpoint callback
            checkpoint_callback = CheckpointCallback(
                save_freq=100_000,  # Save every 100k steps
                save_path=self.model_path,
                name_prefix=self.model_prefix,
                save_replay_buffer=True,
                save_vecnormalize=True
            )

            # Train the agent
            model.learn(total_timesteps=2_000_000, callback=checkpoint_callback)
            
            # Save the final model
            model.save(os.path.join(self.model_path, self.model_prefix))
        finally:
            env.close()

    def run(self):
        """Run the trained snake AI model"""
        env = SnakeEnv(
            game_name=self.game_name,
            grid_size_pixels=self.grid_size_pixels,
            grid_num_squares=self.grid_num_squares,
            framerate=self.framerate,
            inputs_enabled=self.inputs_enabled,
            rendering_enabled=self.rendering_enabled,
            debug=self.debug
        )
        model = PPO.load(os.path.join(self.model_path, self.model_prefix),
                         device="cpu"
        )
        
        obs, _ = env.reset()
        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)

            env.render()
            pygame.time.wait(50)
            
            if terminated or truncated:
                obs, _ = env.reset()
                
            if env.tgame.is_terminated:
                env.close()
                break