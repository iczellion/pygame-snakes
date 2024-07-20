
Training course: https://www.coursera.org/learn/complete-reinforcement-learning-system/

Reward:
    - snake dies: -1000
    - eat food: +10
    - snake moves a block: -1

Action:
    [1, 0, 0] -> straight (up arrow key)
    [0, 1, 0] -> right turn (right arrow key)
    [0, 0, 1] -> left turn (left arrow key)

    * All of these are based on current direction

State (11 values):

    [
    danger straight, danger right, danger left

    direction left, direction right, direction up, direction down

    food left, food right, food up, food down
    ]

    * All of these are boolean values (0, 1)