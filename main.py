import time
import pygame


from tile import Map
from camera import Camera

from loops import main_loop

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
map = Map()
cam = Camera( [0, 0], 1, screen, map )


main_loop( cam, map, screen )
