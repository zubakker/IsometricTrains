import time
import pygame

from camera import Camera
from tile import Tile
from construction import Rail
from cart import Cart

from constants import SCREEN_SIZE


def main_loop( cam, map, screen, trains_list, constr_pack, cart_pack ):
    selected_tile = "default_basic_tile" 
    selected_constr = 0
    facing_list = "NESW"
    facing = 0

    while True:
        keys = pygame.key.get_pressed()
        rail_types = list(constr_pack["rail types"])
        cart_types = list(cart_pack["cart types"])
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left
                    mouse_pos = pygame.mouse.get_pos()
                    pos = cam.get_tile( mouse_pos, map )
                    if selected_constr <= len(rail_types):
                        const = Rail( rail_types[selected_constr-1], 
                                    facing_list[facing], constr_pack )
                        map.set_construction( pos, const )
                        cam.render_bg( map )
                    elif selected_constr:
                        selected_cart = selected_constr - len(rail_types) - 1
                        list_pos = [int(x) for x in pos.split(",")]
                        height = map[ pos ][0].get_height()
                        cart = Cart( cart_pack, cart_types[selected_cart], 
                                     facing_list[facing], list_pos, height )
                        trains_list[0].add_cart(cart)
                    else:
                        map[ pos ][0].change_height(1)
                        map[ pos ][0].change_name( selected_tile )
                        cam.render_bg( map )
                if event.button == 3: # right
                    mouse_pos = pygame.mouse.get_pos()
                    pos = cam.get_tile( mouse_pos, map )
                    map[ pos ][0].change_height(-1)
                    map[ pos ][0].change_name( selected_tile )
                    cam.render_bg( map )
                        
                if event.button == 4: # scroll up
                    if keys[ pygame.K_LSHIFT ]:
                        selected_constr += 1
                        selected_constr = min(len(rail_types) , selected_constr)
                    else:
                        cam.zoom_in(1)
                if event.button == 5: # scroll down
                    if keys[ pygame.K_LSHIFT ]:
                        selected_constr -= 1
                        selected_constr = max(0, selected_constr)
                    else:
                        cam.zoom_in(-1)
            if event.type == pygame.KEYDOWN:
                for i in range(len(rail_types) + len(list(cart_pack["cart types"]))):
                    if event.key == (pygame.K_1 + i):
                        selected_constr = i+1

                
                if event.key == pygame.K_0:
                    selected_tile = "default_bright_tile" 
                    selected_constr = None
                if event.key == pygame.K_w:
                    a = time.time()
                    cam.render_bg( map )
                    print(time.time() -a)
                if event.key == pygame.K_j:
                    cam.move_vert( -1, map )
                if event.key == pygame.K_k:
                    cam.move_vert( +1, map )
                if event.key == pygame.K_r:
                    facing = (facing+1)%4

                    ...
        if keys[ pygame.K_LEFT ] and keys[ pygame.K_LSHIFT ]:
            cam.move( [-0.1, 0] )
        if keys[ pygame.K_LEFT ]:
            cam.move( [-0.0333, 0] )
        if keys[ pygame.K_RIGHT ] and keys[ pygame.K_LSHIFT ]:
            cam.move( [0.1, 0] )
        if keys[ pygame.K_RIGHT ]:
            cam.move( [0.0333, 0] )
        if keys[ pygame.K_UP ] and keys[ pygame.K_LSHIFT ]:
            cam.move( [0, -0.1] )
        if keys[ pygame.K_UP ]:
            cam.move( [0, -0.0333] )
        if keys[ pygame.K_DOWN ] and keys[ pygame.K_LSHIFT ]:
            cam.move( [0, 0.1] )
        if keys[ pygame.K_DOWN ]:
            cam.move( [0, 0.0333] )


        for train in trains_list:
            train.update( map )

        screen.fill( (0, 0, 0) )
        a = time.time()
        cam.render( map, trains_list )
        render_buttons( cam, screen, selected_constr, constr_pack, cart_pack, facing )
        pygame.display.update()
        time.sleep( 0.01 )

def render_buttons( cam, screen, selected_constr, constr_pack, cart_pack, facing ):
    facing_list = "NESW"
    dx, dy = cam.get_default_size()
    dx *= 0.6
    dy *= 0.6
    j = 0
    rail_types = list(constr_pack["rail types"]) + list(cart_pack["cart types"])
    for rail_type in rail_types:
        texture = cam.get_texture( rail_type + "_" + facing_list[facing] )
        if rail_types[selected_constr - 1] == rail_type:
            texture_scaled = pygame.transform.scale( texture, (dx*1.3, dy*1.3) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy*1.3) )
            j += 1.3
        else:
            texture_scaled = pygame.transform.scale( texture, (dx, dy) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy) )
            j += 1
