import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
import pygame

from envs.snake_env import SnakeEnv

class ScoreLoggingCallback(BaseCallback):
    """
    Custom callback for logging the score (from `info["score"]`) 
    to TensorBoard after each episode ends.
    """
    def __init__(self, verbose=0):
        super(ScoreLoggingCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        """
        This method is called after each call to `env.step()`.
        We check if any of the parallel environments is done.
        If done, log the final episode score to TensorBoard.
        """
        # self.locals is a dict of local variables from the RL algorithm
        # "dones" is a list indicating whether the episode finished
        # in each parallel environment
        dones = self.locals["dones"]
        infos = self.locals["infos"]
        
        for i, done in enumerate(dones):
            if done:
                # If the episode is over, we can fetch the "score" from info
                if "score" in infos[i]:
                    episode_score = infos[i]["score"]
                    # Log it to TensorBoard
                    self.logger.record("custom/episode_score", episode_score)

        # By returning True, we tell SB3 to keep training
        return True

class AIController:
    def __init__(self, game_name: str, grid_size_pixels: int, grid_num_squares: int, framerate: int, scratch_dir: str, model_checkpoints_dir: str, training_run_prefix: str, inputs_enabled: bool = False, rendering_enabled: bool = False, debug: bool = False):
        self.game_name = game_name
        self.grid_size_pixels = grid_size_pixels
        self.grid_num_squares = grid_num_squares
        self.framerate = framerate
        self.inputs_enabled = inputs_enabled
        self.rendering_enabled = rendering_enabled
        self.debug = debug
        self.scratch_dir = scratch_dir
        self.model_path = os.path.join(self.scratch_dir, model_checkpoints_dir)
        self.model_prefix = "snake_ppo_model"
        self.training_run_prefix = training_run_prefix

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
                    learning_rate=0.00001,
                    n_steps=2048,
                    batch_size=256,
                    n_epochs=20,
                    tensorboard_log="./.tmp/tensorboard"
            )

            # Create checkpoint callback
            checkpoint_callback = CheckpointCallback(
                save_freq=100_000,  # Save every 100k steps
                save_path=os.path.join(self.model_path, self.training_run_prefix),
                name_prefix=self.model_prefix,
                save_replay_buffer=True,
                save_vecnormalize=True
            )

            score_logging_callback = ScoreLoggingCallback()

            # Train the agent
            model.learn(total_timesteps=20_000_000
                        ,callback=[checkpoint_callback, score_logging_callback]
                        ,tb_log_name=f"{self.training_run_prefix}"
            )

            # Save the final model
            model.save(os.path.join(self.model_path, self.training_run_prefix, self.model_prefix))
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
        model = PPO.load(os.path.join(self.model_path, self.training_run_prefix, self.model_prefix),
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