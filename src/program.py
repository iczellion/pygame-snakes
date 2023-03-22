import pygame

from game import TGame
from render import Renderer
from snake import TSnake, Orientation

def main():
    
    tgame = TGame.initialize(game_name="Snake", grid_size_pixels=600, grid_num_squares=20)
    tgame.create_snake()
    tgame.create_apple()

    pygame.init()
    pygame.display.set_caption(tgame.game_name)
    
    screen = pygame.display.set_mode((tgame.grid_size_pixels, tgame.grid_size_pixels))
    render = Renderer(screen)
    
    # change the value to False, to exit the main loop
    running = True
    
    clock = pygame.time.Clock()

    # main loop
    while running:

        if tgame.tsnake.is_alive == False:
            tgame.create_snake()

        render.draw_background()
        #render.draw_grid(tgame.grid_size_pixels, tgame.grid_num_squares)
        render.draw_snake(tgame, tgame.tsnake)
        render.draw_apple(tgame, tgame.apple_coords)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tgame.tsnake.head_orientation != Orientation.RIGHT:
                    tgame.tsnake.head_orientation = Orientation.LEFT
                elif event.key == pygame.K_RIGHT and tgame.tsnake.head_orientation != Orientation.LEFT:
                    tgame.tsnake.head_orientation = Orientation.RIGHT
                elif event.key == pygame.K_UP and tgame.tsnake.head_orientation != Orientation.DOWN:
                    tgame.tsnake.head_orientation = Orientation.UP
                elif event.key == pygame.K_DOWN and tgame.tsnake.head_orientation != Orientation.UP:
                    tgame.tsnake.head_orientation = Orientation.DOWN

        tgame.tsnake.move_snake(tgame.tsnake.head_orientation)

        if(tgame.is_snake_colliding_with_apple()):
            tgame.tsnake.grow_snake()
            tgame.create_apple()

        # Check if snake is out of bounds
        # If it is, it means we are dead and should restart
        if tgame.coord_is_out_of_bound((tgame.tsnake.head_x, tgame.tsnake.head_y)):
            tgame.tsnake.is_alive = False
            tgame.set_score(0)

        #pygame.display.update()
        pygame.display.flip()

        clock.tick(8)
    
    pygame.quit()
    quit()

if __name__=="__main__":
    main()