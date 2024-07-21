import pygame

from game import TGame
from snake import TSnake, Orientation

class Renderer:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
    
    def draw_background(self):
        black_color = (0, 0, 0)

        # draw background
        self.screen.fill(black_color) # Fill black

    def draw_grid(self, grid_size_pixels: int, grid_num_squares: int):
        white_color = (200, 200, 200)
        size_of_one_square = int(grid_size_pixels / grid_num_squares)
        
        # draw grid
        for x in range(0, grid_size_pixels, size_of_one_square):
            for y in range(0, grid_size_pixels, size_of_one_square):
                rect = pygame.Rect(x, y, size_of_one_square, size_of_one_square)
                pygame.draw.rect(self.screen, white_color, rect, 1)

    def draw_snake(self, tgame: TGame, tsnake: TSnake):
        head_color = (0, 0, 255)
        body_color = (0, 0, 100)
        size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares

        # draw head
        rect_head = pygame.Rect(tsnake.head_x * size_of_one_square, tsnake.head_y * size_of_one_square, size_of_one_square, size_of_one_square)
        pygame.draw.rect(self.screen, head_color, rect_head)

        # draw body
        for sp in tsnake.snake_parts:
            rect_body = pygame.Rect(sp[0] * size_of_one_square, sp[1] * size_of_one_square, size_of_one_square, size_of_one_square)
            pygame.draw.rect(self.screen, body_color, rect_body)

    def draw_apple(self, tgame: TGame, apple: tuple):
        apple_color = (255, 0, 0)
        size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares

        # draw
        rect_apple = pygame.Rect(apple[0] * size_of_one_square, apple[1] * size_of_one_square, size_of_one_square, size_of_one_square)
        pygame.draw.rect(self.screen, apple_color, rect_apple)