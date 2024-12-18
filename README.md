# pygame-snakes

A Snake game implementation using Python and Pygame, featuring both interactive gameplay and AI learning capabilities through reinforcement learning.

## Features

- Classic Snake gameplay with keyboard controls
- AI mode using Reinforcement Learning (PPO algorithm)
- Training mode to teach the AI
- Configurable grid size and game speed
- Score tracking
- Debug mode for development

## Requirements

- Python 3.12.x
- Poetry 1.8.x

## Installation

Install dependencies using Poetry:
```shell
poetry install
```

## Usage

Activate the virtual environment:
```shell
poetry shell
```

The game supports three modes:

### 1. Interactive Mode
Play the classic Snake game using arrow keys:
```shell
python src/main.py int
```

### 2. AI Mode
Watch the trained AI play Snake:
```shell
python src/main.py ai
```

### 3. Training Mode
Train the AI model:
```shell
python src/main.py train
```

### Additional Options

- Add `--debug` flag to enable debug visualization:
```shell
python src/main.py int --debug
```

### Training Visualization

Monitor the training progress using TensorBoard:
```shell
tensorboard --logdir ./.tmp/tensorboard
```

## Project Structure

- `src/main.py` - Main entry point
- `src/game.py` - Core game logic
- `src/snake.py` - Snake entity implementation
- `src/ai_controller.py` - AI training and execution
- `src/envs/snake_env.py` - Gymnasium environment for AI