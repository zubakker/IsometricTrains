import time
import pygame


from tile import Map, Tile
from camera import Camera
from cart import Cart, Train
from construction import Rail, load_construction_pack

from loops import main_loop

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
map = Map()
cam = Camera( [0, 0], 1, screen, map )



# TEMP
cart1 = Cart( "default_cart", "N", [0, 1], 0 )
cart2 = Cart( "default_cart", "N", [0, 0], 0 )

train = Train(0.03, [cart1, cart2])
trains_list = list()
trains_list.append(train)
 
c_pack = load_construction_pack("default_rail")
construction1 = Rail("default_rail_straight", "N", c_pack)
construction2 = Rail("default_rail_straight", "N", c_pack)
map.set_construction('0,0', construction1)
map.set_construction('0,1', construction2)


main_loop( cam, map, screen, trains_list, c_pack )
