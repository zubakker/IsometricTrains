import time
import pygame


from tile import Map
from camera import Camera

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
map = Map()
cam = Camera( [0, 0], 1, screen, map )


while True:
    pygame.display.update()

    cam.render( map )

    time.sleep( 0.01 )
