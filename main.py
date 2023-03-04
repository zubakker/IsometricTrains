import time
import pygame


from tile import Map
from camera import Camera
from cart import Cart
from construction import load_construction_pack

from loops import main_loop

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
map = Map()
cam = Camera( [0, 0], 1, screen, map )

# TEMP
cart = Cart( "default_cart", "N", [0, 0] )
trains_list = list()
trains_list.append(cart)
# 
c_pack = load_construction_pack("default_rail")


main_loop( cam, map, screen, trains_list, c_pack )
