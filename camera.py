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
        map.load_chunck( [position[0]//2,  position[1]//2] )

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
        y_0 = -8
        y_1 = 8 
        x_0 = -8
        x_1 = 8 
        ...
        for i in range( y_0, y_1 ):
            for j in range( x_0, x_1 ):
                # ... NOT RECOGNIZING HEIGHT ...
                position = [ i - self.position[0], j - self.position[1] ]
                tile = map[ str(i)+","+str(j) ]
                position[1] += tile.get_height()*2
                tile_img = self.texture_pack[ tile.get_name() ] 
                size_x = self.default_tile_size[0] * self.zoom
                size_y = self.default_tile_size[1] * self.zoom
                tile_img_scaled = pygame.transform.scale( tile_img, (size_x, size_y) )
                pos_x = (position[0] + j/2) * self.default_tile_size[0] * self.zoom
                pos_y = position[1]/2 * self.default_tile_size[1] * self.zoom
                self.screen.blit( tile_img_scaled, 
                            (pos_x + SCREEN_SIZE[0]/2,
                             pos_y + SCREEN_SIZE[1]/2)
                        )
        # === rendering trains ===
        ...

    def move( self ): # ...
        # if y_0 or y_1 or x_0 or x_1 not in map 
        #   (not loaded, bc camera moved too far)
        map.load_chunck( ... )
