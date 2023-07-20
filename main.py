import time
import pygame


from tile import Map, Tile
from camera import Camera
from cart import Cart, Train, load_cart_pack
from construction import Rail, load_construction_pack

from loops import main_loop, load_button_pack

from constants import SCREEN_SIZE

screen = pygame.display.set_mode( SCREEN_SIZE )
cart_pack = load_cart_pack("default_cart")
constr_pack = load_construction_pack("default_rail")
button_pack = load_button_pack("default_button")
map = Map( constr_pack, cart_pack )
cam = Camera( [0, 0], 0.25, screen, map, constr_pack, cart_pack )



# TEMP
cart1 = Cart( cart_pack, "default_engine", "N", [-1, 1], 0 )
cart2 = Cart( cart_pack, "default_cart", "N", [-1, 0], 0 )
cart3 = Cart( cart_pack, "default_cart", "N", [-1, -1], 0 )

train = Train( cart_pack, [cart1, cart2, cart3])
trains_list = list()
trains_list.append(train)

button_path = ''
 

main_loop( cam, map, screen, trains_list, button_path,
        constr_pack, cart_pack, button_pack )
