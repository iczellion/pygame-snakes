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

    def draw_grid(self, tgame: TGame):
        white_color = (200, 200, 200)

        size_of_one_square = int(tgame.grid_size_pixels / tgame.grid_num_squares)
        
        # draw grid
        for x in range(0, tgame.grid_size_pixels, size_of_one_square):
            for y in range(0, tgame.grid_size_pixels, size_of_one_square):
                rect = pygame.Rect(x, y, size_of_one_square, size_of_one_square)
                pygame.draw.rect(self.screen, white_color, rect, 1)

    def draw_snake(self, tgame: TGame):
        head_color = (0, 0, 255)
        body_color = (0, 0, 100)
        size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares

        # draw head
        rect_head = pygame.Rect(tgame.tsnake.head_x * size_of_one_square, tgame.tsnake.head_y * size_of_one_square, size_of_one_square, size_of_one_square)
        pygame.draw.rect(self.screen, head_color, rect_head)

        # draw body
        for sp in tgame.tsnake.snake_parts:
            rect_body = pygame.Rect(sp[0] * size_of_one_square, sp[1] * size_of_one_square, size_of_one_square, size_of_one_square)
            pygame.draw.rect(self.screen, body_color, rect_body)

    def draw_apple(self, tgame: TGame):
        apple_color = (255, 0, 0)
        size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares

        # draw
        apple_x = tgame.apple_coords[0]
        apple_y = tgame.apple_coords[1]
        rect_apple = pygame.Rect(apple_x * size_of_one_square, apple_y * size_of_one_square, size_of_one_square, size_of_one_square)
        pygame.draw.rect(self.screen, apple_color, rect_apple)
    
    def draw_fov(self, tgame: TGame):
        fov_color = (195, 195, 195)
        fov_distance = tgame.fov_distance
        size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares
        fov_top_x_pixel = (tgame.tsnake.head_x * size_of_one_square) - (fov_distance * size_of_one_square)
        head_top_y_pixel = (tgame.tsnake.head_y * size_of_one_square) - (fov_distance * size_of_one_square)
        fov_area = (fov_distance * size_of_one_square * 2) + size_of_one_square

        rect_area = pygame.Rect(fov_top_x_pixel, head_top_y_pixel, fov_area, fov_area)
        pygame.draw.rect(self.screen, fov_color, rect_area)

    def render_all(self, tgame: TGame, debug: bool = False):
        self.draw_background()

        if debug:
            self.draw_fov(tgame)
            self.draw_grid(tgame)

        self.draw_snake(tgame)
        self.draw_apple(tgame)