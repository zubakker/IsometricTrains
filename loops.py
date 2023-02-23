import time
import pygame



def main_loop( cam, map, screen ):
    while True:
        for event in pygame.event.get():
            pass
        keys = pygame.key.get_pressed()
        if keys[ pygame.K_LEFT ]:
            cam.move( [-1, 0] )
        if keys[ pygame.K_RIGHT]:
            cam.move( [1, 0] )
        if keys[ pygame.K_UP ]:
            cam.move( [0, -1] )
        if keys[ pygame.K_DOWN ]:
            cam.move( [0, 1] )

        screen.fill( (0, 0, 0) )
        cam.render( map )
        pygame.display.update()
        time.sleep( 0.05 )

