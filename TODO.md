# Change features

https://www.youtube.com/watch?v=-kUolVQdNf0
35 secondes


# Experiment 20241226_1003

Remove Wall checks (directly adjacent)
```
wall_up = 1 if head_y - 1 < 0 else 0
wall_right = 1 if head_x + 1 >= grid_size else 0
wall_down = 1 if head_y + 1 >= grid_size else 0
wall_left = 1 if head_x - 1 < 0 else 0
```

Remove Snake body checks (directly adjacent)
```
snake_up = 1 if (head_x, head_y - 1) in snake_body else 0
snake_right = 1 if (head_x + 1, head_y) in snake_body else 0
snake_down = 1 if (head_x, head_y + 1) in snake_body else 0
snake_left = 1 if (head_x - 1, head_y) in snake_body else 0
```

# Experiment 20241226_1051

Add corridor feature
```
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
```

# Experiment 20241227_1322

Implement BFS algorithm


# Experiment 20241227_2306

Tweak hyperparameters in ai_controller.py
```
learning_rate=0.00001
batch_size=256
n_epochs=20
total_timesteps=10_000_000
```