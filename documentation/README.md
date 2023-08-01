Reward:
    - eat food: +10
    - game over: -10
    - else: 0

Action:
    [1, 0, 0] -> straight
    [0, 1, 0] -> right turn
    [0, 0, 1] -> left turn

    * All of these are based on current direction

State (11 values):

    [
    danger straight, danger right, danger left

    direction left, direction right, direction up, direction down

    food left, food right, food up, food down
    ]

    * All of these are boolean values (0, 1)