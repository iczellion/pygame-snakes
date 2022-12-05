import pygame

from game import TGame
from snake import TSnake, Orientation

def draw_background(screen):
    black_color = (0, 0, 0)

    # draw background
    screen.fill(black_color) # Fill black

def draw_grid(screen, grid_size_pixels: int, grid_num_squares: int):
    white_color = (200, 200, 200)
    
    # draw grid
    for x in range(0, grid_size_pixels, grid_num_squares):
        for y in range(0, grid_size_pixels, grid_num_squares):
            rect = pygame.Rect(x, y, grid_num_squares, grid_num_squares)
            pygame.draw.rect(screen, white_color, rect, 1)

def draw_snake(screen, tgame: TGame, tsnake: TSnake):
    head_color = (255, 0, 0)
    body_color = (0, 0, 255)
    size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares

    # draw head
    rect_head = pygame.Rect(tsnake.head_x, tsnake.head_y, size_of_one_square, size_of_one_square)
    pygame.draw.rect(screen, head_color, rect_head)

    # draw body
    for sp in tsnake.snake_parts:
        rect_body = pygame.Rect(sp[0], sp[1], size_of_one_square, size_of_one_square)
        pygame.draw.rect(screen, body_color, rect_body)

def main():
    
    tgame = TGame.initialize(game_name="Snake", grid_size_pixels=400, grid_num_squares=20)
    size_of_one_square = tgame.grid_size_pixels / tgame.grid_num_squares
    orientation = Orientation.RIGHT

    tsnake = TSnake(size_of_one_square, orientation)

    pygame.init()
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption(tgame.game_name)
    
    screen = pygame.display.set_mode((tgame.grid_size_pixels, tgame.grid_size_pixels))
    
    # change the value to False, to exit the main loop
    running = True
    
    clock = pygame.time.Clock()

    # main loop
    while running:

        draw_background(screen)
        draw_grid(screen, tgame.grid_size_pixels, tgame.grid_num_squares)
        draw_snake(screen, tgame, tsnake)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    orientation = Orientation.LEFT
                elif event.key == pygame.K_RIGHT:
                    orientation = Orientation.RIGHT
                elif event.key == pygame.K_UP:
                    orientation = Orientation.UP
                elif event.key == pygame.K_DOWN:
                    orientation = Orientation.DOWN

        tsnake.move_snake(orientation)

        #pygame.display.update()
        pygame.display.flip()

        clock.tick(10)
    
    pygame.quit()
    quit()

if __name__=="__main__":
    main()