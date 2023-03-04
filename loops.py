import time
import pygame

from camera import Camera
from tile import Tile
from construction import Rail

from constants import SCREEN_SIZE


def main_loop( cam, map, screen, trains_list, c_pack ):
    selected_tile = "default_bright_tile" 
    selected_constr = None
    facing_list = [ "N", "E", "NE", "NW", "SE", "SW" ]
    facing = None 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left
                    mouse_pos = pygame.mouse.get_pos()
                    pos = cam.get_tile( mouse_pos )
                    if selected_constr:
                        const = Rail( selected_constr, facing, c_pack )
                        map.set_construction( pos, const )
                        cam.render_bg( map )
                    else:
                        tile = Tile( selected_tile, 0 )
                        map.set_tile( pos, tile )
                        cam.render_bg( map )
                        
                if event.button == 4: # scroll up
                    cam.zoom_in(1)
                if event.button == 5: # scroll down
                    cam.zoom_in(-1)
            if event.type == pygame.KEYDOWN:
                for i in range(6):
                    if event.key == (pygame.K_1 + i):
                        selected_constr = "default_rail_" + facing_list[i]
                        facing = facing_list[i]

                if event.key == pygame.K_7:
                    selected_constr = "default_junction_rail_NES"
                    facing = "NES"
                if event.key == pygame.K_8:
                    selected_constr = "default_junction_rail_NESW"
                    facing = "NESW"
                
                if event.key == pygame.K_0:
                    selected_tile = "default_bright_tile" 
                    selected_constr = None
                if event.key == pygame.K_w:
                    cam.render_bg( map )
                    ...
        keys = pygame.key.get_pressed()
        if keys[ pygame.K_LEFT ]:
            cam.move( [-0.333, 0] )
        if keys[ pygame.K_RIGHT]:
            cam.move( [0.333, 0] )
        if keys[ pygame.K_UP ]:
            cam.move( [0, -0.333] )
        if keys[ pygame.K_DOWN ]:
            cam.move( [0, 0.333] )

        for train in trains_list:
            train.update( map )

        screen.fill( (0, 0, 0) )
        cam.render( map, trains_list )
        render_buttons( cam, screen, selected_constr )
        pygame.display.update()
        time.sleep( 0.01 )

def render_buttons( cam, screen, selected_constr ):
    dx, dy = cam.get_default_size()
    j = 0
    for i in [ "N", "E", "NE", "NW", "SE", "SW" ]:
        texture = cam.get_texture( "default_rail_" + i )
        if selected_constr == "default_rail_" + i:
            texture_scaled = pygame.transform.scale( texture, (dx*1.3, dy*1.3) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy*1.3) )
            j += 1.3
        else:
            texture_scaled = pygame.transform.scale( texture, (dx, dy) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy) )
            j += 1
    for i in ["NES", "NESW"]:
        texture = cam.get_texture( "default_junction_rail_" + i )
        if selected_constr == "default_junction_rail_" + i:
            texture_scaled = pygame.transform.scale( texture, (dx*1.3, dy*1.3) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy*1.3) )
            j += 1.3
        else:
            texture_scaled = pygame.transform.scale( texture, (dx, dy) )
            screen.blit( texture_scaled, ((dx+5)*j, SCREEN_SIZE[1]-dy) )
            j += 1

    # screen.blit( north_img, (0, SCREEN_SIZE[1]-dy) )
