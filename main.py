import time
import pygame


from tile import Map, Tile
from camera import Camera
from cart import Cart, Train, load_cart_pack
from construction import Rail, load_construction_pack

from loops import main_loop

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
cart_pack = load_cart_pack("default_cart")
constr_pack = load_construction_pack("default_rail")
map = Map( constr_pack, cart_pack )
cam = Camera( [0, 0], 1, screen, map, constr_pack, cart_pack )



# TEMP
cart1 = Cart( cart_pack, "default_cart", "N", [-1, 1], 0 )
# cart2 = Cart( cart_pack, "default_cart", "N", [-1, 0], 0 )
# cart3 = Cart( cart_pack, "default_cart", "N", [-1, -1], 0 )

train = Train( cart_pack, [cart1]) # , cart2, cart3])
trains_list = list()
trains_list.append(train)
 

main_loop( cam, map, screen, trains_list, constr_pack, cart_pack )
