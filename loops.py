import time
import pygame

from json import loads

from camera import Camera
from tile import Tile
from construction import Rail, Station
from cart import Cart

from cart import load_trains_list, save_trains_list

from constants import SCREEN_SIZE, DEFAULT_SAVE_PATH, DEFAULT_TILE_SIZE, DEFAULT_BUTTON_SIZE

def load_button_pack( name ):
    inp = open("button_packs/" + name + ".json", "r").read()
    button_pack = loads(inp)
    return button_pack

def get_buttons( path, constr_pack, cart_pack, button_pack, tile_list, facing ):
    facing_list = "NESW"
    angle_list = [ 
            "0.0",
            "1.0",
            "2.0",
            "-1.0"
                ]
    sep_path = path.split("/")
    stage = button_pack
    for menu in sep_path:
        stage = stage[menu]["buttons"]
    if path:
        stage["back"] = button_pack[""]["back"]

    # TEMP starts:
    if menu == "rail":
        rail_types = list(constr_pack["rail types"]) + list(constr_pack["station types"])
        for rail_type in rail_types:
            if rail_type.endswith("_nr") or rail_type.endswith("_nb"):
                continue
            stage[rail_type] = {
                    "texture_name": rail_type+"_"+facing_list[facing],
                    "texture_scale": [1, 0.5]
            }
    if menu == "terrain":
        for tile_type in tile_list:
            if tile_type.endswith("_nr") or tile_type.endswith("_nb"):
                continue
            stage[tile_type] = {
                    "texture_name": tile_type,
                    "texture_scale": [1, 0.5]
            }
    if menu == "train":
        for cart_type in list(cart_pack["cart types"]):
            if cart_type.endswith("_nr") or cart_type.endswith("_nb"):
                continue
            stage[cart_type] = {
                    "texture_name": cart_type+"_"+angle_list[facing]+",0.0",
                    "texture_scale": [1, 1.18]
            }
            ...
    # :TEMP ends
    return stage

def enter_submenu( selected_button, path,
        constr_pack, cart_pack, button_pack, tile_list, facing ):
    buttons = get_buttons(path, constr_pack, cart_pack, button_pack, tile_list, facing)
    if selected_button > len(list(buttons)):
        return path, None
    if list(buttons)[selected_button-1] == "back":
        path = "/".join( path.split("/")[:-1])
        return path, None
    else:
        menu = list(buttons)[selected_button-1]
        if "buttons" not in buttons[menu]:
            return path, menu
    return path + "/" + menu, None



def main_loop( cam, map, screen, trains_list, button_path,
        constr_pack, cart_pack, button_pack ):
    selected_button = 0
    selected_build = None
    facing_list = "NESW"
    facing = 0 
    tile_list = cam.get_tile_list()
    rail_types = list(constr_pack["rail types"]) # DEL 
    station_types = list(constr_pack["station types"]) # DEL 
    cart_types = list(cart_pack["cart types"]) # DEL 

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left
                    mouse_pos = pygame.mouse.get_pos()
                    pos = cam.get_tile( mouse_pos, map )

                    if not selected_build:
                        continue

                    if "rail" in selected_build:
                        const = Rail( selected_build, 
                                    facing_list[facing], constr_pack )
                        map.set_construction( pos, const )
                        cam.render_bg( map )
                    if "station" in selected_build:
                        const = Station( selected_build, 
                                    facing_list[facing], constr_pack )
                        map.set_construction( pos, const )
                        cam.render_bg( map )
                    if "tile" in selected_build:
                        map[ pos ][0].change_name( selected_build )
                        cam.render_bg( map )
                    if "cart" in selected_build:
                        list_pos = [int(x) for x in pos.split(",")]
                        height = map[ pos ][0].get_height()
                        cart = Cart( cart_pack, selected_build, 
                                     facing_list[facing], list_pos, height )
                        trains_list[0].add_cart(cart) # TEMP
                        '''
                    else:
                        map[ pos ][0].change_height(1)
                        map[ pos ][0].change_name( selected_tile )
                        cam.render_bg( map )
                        '''
                if event.button == 3: # right
                    mouse_pos = pygame.mouse.get_pos()
                    pos = cam.get_tile( mouse_pos, map )
                    map[ pos ][0].change_height(-1)
                    map[ pos ][0].change_name( selected_tile )
                    cam.render_bg( map )
                        
                if event.button == 4: # scroll up
                    if keys[ pygame.K_LSHIFT ]:
                        selected_button += 1
                        selected_button = min(len(rail_types)+len(cart_types)+len(station_types) , selected_button)
                    else:
                        cam.zoom_in(1)
                if event.button == 5: # scroll down
                    if keys[ pygame.K_LSHIFT ]:
                        selected_button -= 1
                        selected_button = max(0, selected_button)
                    else:
                        cam.zoom_in(-1)
            if event.type == pygame.KEYDOWN:
                for i in range(len(rail_types) + len(list(cart_pack["cart types"]))):
                    if event.key == (pygame.K_1 + i):
                        selected_button = i+1
                        button_path, selected_build = enter_submenu(selected_button, 
                                button_path, constr_pack, cart_pack, 
                                button_pack, tile_list, facing)
                        if not selected_build:
                            selected_button = 0


                
                if event.key == pygame.K_0:
                    selected_tile = "default_tile" 
                    selected_button = 0
                if event.key == pygame.K_j:
                    cam.move_vert( -1, map )
                if event.key == pygame.K_k:
                    cam.move_vert( +1, map )
                if event.key == pygame.K_r:
                    facing = (facing+1)%4

                if event.key == pygame.K_w:
                    map.save_chunck([0,0], DEFAULT_SAVE_PATH, trains_list) # TEMP
                    save_trains_list(trains_list, DEFAULT_SAVE_PATH)
                if event.key == pygame.K_s:
                    trains_list = load_trains_list(DEFAULT_SAVE_PATH, cart_pack)

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
        cam.render( map, trains_list, cart_pack )
        render_buttons( cam, screen, selected_button, button_path,
                constr_pack, cart_pack, button_pack, facing )
        pygame.display.update()
        time.sleep( 0.01 )

def render_buttons( cam, screen, selected_button, button_path,
        constr_pack, cart_pack, button_pack, facing ):
    dx, dy = DEFAULT_BUTTON_SIZE
    dx *= 0.6
    dy *= 0.6
    j = 0
    i = 0
    tile_list = cam.get_tile_list()

    for name, button in get_buttons(button_path, constr_pack, 
            cart_pack, button_pack, tile_list, facing).items():
        i += 1
        texture = cam.get_texture( button["texture_name"], ignore_zoom=True )
        if selected_button == i:
            scale_x = dx * button["texture_scale"][0]
            scale_y = dy * button["texture_scale"][1]
            texture_scaled = pygame.transform.scale( texture, (scale_x*1.3, scale_y*1.3) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy*1.3) )
            j += 1.3
        else:
            scale_x = dx * button["texture_scale"][0]
            scale_y = dy * button["texture_scale"][1]
            texture_scaled = pygame.transform.scale( texture, (scale_x, scale_y) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy) )
            j += 1
