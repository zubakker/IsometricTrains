import time
import pygame


from tile import Map, Tile
from camera import Camera
from cart import Cart, Train, load_cart_pack
from construction import Rail, load_construction_pack

from loops import main_loop

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
map = Map()
cam = Camera( [0, 0], 1, screen, map )



# TEMP
cart_pack = load_cart_pack("default_cart")
cart1 = Cart( cart_pack, "default_engine", "N", [0, 1], 0 )
cart2 = Cart( cart_pack, "default_cart", "N", [0, 0], 0 )
cart3 = Cart( cart_pack, "default_cart", "N", [0, -1], 0 )

train = Train([cart1, cart2, cart3])
trains_list = list()
trains_list.append(train)
 
constr_pack = load_construction_pack("default_rail")
construction1 = Rail("default_rail_straight", "N", constr_pack)
# construction3 = Rail("default_rail_curved", "S", constr_pack)
# construction4 = Rail("default_rail_curved", "W", constr_pack)
# construction5 = Rail("default_rail_curved", "N", constr_pack)
# construction6 = Rail("default_rail_curved", "E", constr_pack)
map.set_construction('0,1', construction1)
map.set_construction('0,0', construction1)
map.set_construction('0,-1', construction1)
# map.set_construction('1,0', construction1)
# map.set_construction('1,-1', construction2)
# map.set_construction('0,1', construction2)
# map.set_construction('0,1', construction3)
# map.set_construction('1,1', construction4)
# map.set_construction('1,-2', construction5)
# map.set_construction('0,-2', construction6)


main_loop( cam, map, screen, trains_list, constr_pack, cart_pack )
