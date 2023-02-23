import os
import pygame


from tile import Tile, Map

from constants import SCREEN_SIZE


class Camera:
    position: [float, float]
    zoom: float
    texture_pack: dict
    screen: pygame.display
    default_tile_size: [float, float]

    def __init__( self, position, zoom, screen, map ):
        self.position = position
        self.zoom = zoom
        self.screen = screen
        self.texture_pack = dict()
        self.load_texture_pack( "default" )
        chunck_size = map.get_chunck_size()
        map.load_chunck( [position[0]//chunck_size, position[1]//chunck_size] )

        self.default_tile_size = [70, 41] # TEMP
        ...

    def load_texture_pack( self, name ):
        full_name = "texture_packs/tiles/" + name
        tile_textures = os.listdir( full_name )
        for texture in tile_textures:
            self.texture_pack[ texture[:-4] ] = pygame.image.load(full_name +"/"+ texture)
        ...
    
    def render( self, map: Map ):
        # === rendering tiles ===
        # -- Define which coords are on screen --
        screen_w_tiles = SCREEN_SIZE[0] / (self.default_tile_size[0] * self.zoom)
        screen_h_tiles = SCREEN_SIZE[1] / (self.default_tile_size[1] * self.zoom)
        x_0 = int(-screen_w_tiles/2 + self.position[0]/2)
        x_1 = int(+screen_w_tiles/2 + self.position[0]/2)

        y_0 = x_0 # TEMP
        y_1 = x_1 # TEMP

        swt = int(screen_w_tiles)
        sht = int(screen_w_tiles) # TEMP
        for i in range( y_0-sht, y_1+sht+1 ): 
                # -sht/swt needed to load 3 chuncks around center of the screen
            for j in range( x_0-swt, x_1+swt+1 ):
                position = [ j - self.position[0], i - self.position[1] ]
                tile = map[ str(j)+","+str(i) ]
                position[1] += tile.get_height()*2
                tile_img = self.texture_pack[ tile.get_name() ] 
                size_x = self.default_tile_size[0] * self.zoom
                size_y = self.default_tile_size[1] * self.zoom
                tile_img_scaled = pygame.transform.scale( tile_img, (size_x, size_y) )
                pos_x = (position[0]/2 + i/2 -0.5) * self.default_tile_size[0] * self.zoom
                pos_y = (position[1] + j/2 -3*i/2) * self.default_tile_size[1] * self.zoom
                self.screen.blit( tile_img_scaled, 
                                    (pos_x + SCREEN_SIZE[0]/2,
                                     pos_y + SCREEN_SIZE[1]/2)
                                )
        # === rendering trains ===
        ...

    def move( self, rel_pos ): # ...
        self.position[0] += rel_pos[0]*self.zoom
        self.position[1] += rel_pos[1]*self.zoom
        # if y_0 or y_1 or x_0 or x_1 not in map 
        #   (not loaded, bc camera moved too far)
