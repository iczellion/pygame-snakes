from __future__ import annotations

import pygame

class Renderer:

    def __init__(self, tgame: TGame):
        pygame.display.set_caption(tgame.game_name)
        self.screen = pygame.display.set_mode((tgame.grid_size_pixels, tgame.grid_size_pixels))
        self.tgame = tgame
    
    def draw_background(self):
        black_color = (0, 0, 0)

        # draw background
        self.screen.fill(black_color) # Fill black

    def draw_grid(self):
        white_color = (200, 200, 200)

        size_of_one_square = int(self.tgame.grid_size_pixels / self.tgame.grid_num_squares)
        
        # draw grid
        for x in range(0, self.tgame.grid_size_pixels, size_of_one_square):
            for y in range(0, self.tgame.grid_size_pixels, size_of_one_square):
                rect = pygame.Rect(x, y, size_of_one_square, size_of_one_square)
                pygame.draw.rect(self.screen, white_color, rect, 1)

    def draw_snake(self):
        head_color = (0, 0, 255)
        body_color = (0, 0, 100)
        size_of_one_square = self.tgame.grid_size_pixels / self.tgame.grid_num_squares

        # draw head
        rect_head = pygame.Rect(self.tgame.tsnake.head_x * size_of_one_square, self.tgame.tsnake.head_y * size_of_one_square, size_of_one_square, size_of_one_square)
        pygame.draw.rect(self.screen, head_color, rect_head)

        # draw body
        for sp in self.tgame.tsnake.snake_parts:
            rect_body = pygame.Rect(sp[0] * size_of_one_square, sp[1] * size_of_one_square, size_of_one_square, size_of_one_square)
            pygame.draw.rect(self.screen, body_color, rect_body)

    def draw_apple(self):
        apple_color = (255, 0, 0)
        size_of_one_square = self.tgame.grid_size_pixels / self.tgame.grid_num_squares

        # draw
        apple_x = self.tgame.apple_coords[0]
        apple_y = self.tgame.apple_coords[1]
        rect_apple = pygame.Rect(apple_x * size_of_one_square, apple_y * size_of_one_square, size_of_one_square, size_of_one_square)
        pygame.draw.rect(self.screen, apple_color, rect_apple)
    
    def draw_fov(self):
        fov_color = (195, 195, 195)
        fov_distance = self.tgame.fov_distance
        size_of_one_square = self.tgame.grid_size_pixels / self.tgame.grid_num_squares
        fov_top_x_pixel = (self.tgame.tsnake.head_x * size_of_one_square) - (fov_distance * size_of_one_square)
        head_top_y_pixel = (self.tgame.tsnake.head_y * size_of_one_square) - (fov_distance * size_of_one_square)
        fov_area = (fov_distance * size_of_one_square * 2) + size_of_one_square

        rect_area = pygame.Rect(fov_top_x_pixel, head_top_y_pixel, fov_area, fov_area)
        pygame.draw.rect(self.screen, fov_color, rect_area)
    
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = f"Score: {self.tgame.score}"
        text_surface = font.render(score_text, True, (255, 255, 255))  # White text
        
        # Position in top right with some padding
        padding = 10
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.tgame.grid_size_pixels - padding, padding)
        
        self.screen.blit(text_surface, text_rect)    

    def render_all(self):
        self.draw_background()

        if self.tgame.debug:
            self.draw_fov()
            self.draw_grid()

        self.draw_snake()
        self.draw_apple()
        self.draw_score()

        pygame.display.flip()