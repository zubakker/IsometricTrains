import os
import pygame


from tile import Tile, Map

from constants import SCREEN_SIZE


class Camera:
    position: [float, float]
    zoom: float
    texture_pack: dict
    background: pygame.Surface
    screen: pygame.Surface
    default_tile_size: [float, float]
    bg_updated: bool

    def __init__( self, position, zoom, screen, map ):
        self.position = position
        self.zoom = zoom
        self.screen = screen
        self.texture_pack = dict()
        self.load_texture_pack( "default" )

        self.bg_updated = False
        self.background = pygame.Surface( (SCREEN_SIZE[0]*3, SCREEN_SIZE[1]*3) )
        self.bg_position = [0, 0]

        chunck_size = map.get_chunck_size()
        map.load_chunck( [position[0]//chunck_size, position[1]//chunck_size] )

        self.default_tile_size = [70, 41] # TEMP
        ...

    def load_texture_pack( self, name ):
        tile_name = "texture_packs/tiles/" + name
        const_name = "texture_packs/constructions/" + name
        cart_name = "texture_packs/carts/" + name
        tile_textures = os.listdir( tile_name )
        const_textures = os.listdir( const_name )
        cart_textures = os.listdir( cart_name )
        for texture in tile_textures:
            self.texture_pack[ texture[:-4] ] = pygame.image.load(tile_name +"/"+ texture)
        for texture in const_textures:
            self.texture_pack[ texture[:-4] ] = pygame.image.load(const_name +"/"+ texture)
        for texture in cart_textures:
            self.texture_pack[ texture[:-4] ] = pygame.image.load(cart_name +"/"+ texture)
        ...
    def get_texture( self, name ):
        if name not in list(self.texture_pack):
            return 0
        return self.texture_pack[name]
    def get_default_size(self):
        return self.default_tile_size
    def get_position( self):
        return self.position

    def render( self, map, trains_list ):
        if not self.bg_updated:
            self.render_bg( map )

        dx = self.position[0] - self.bg_position[0]
        dy = self.position[1] - self.bg_position[1]
        posx = -SCREEN_SIZE[0] - self.default_tile_size[0]*dx*self.zoom
        posy = -SCREEN_SIZE[1] - self.default_tile_size[1]*dy*self.zoom
        if posx > 0 or posy > 0:
            self.render_bg( map )
        if posx + SCREEN_SIZE[0]*2 < 0 or posy + SCREEN_SIZE[1]*2 < 0:
            self.render_bg( map )
        self.screen.blit( self.background,
                (-SCREEN_SIZE[0] - self.default_tile_size[0]*dx*self.zoom,
                -SCREEN_SIZE[1] - self.default_tile_size[1]*dy*self.zoom) )
        # -- Rendering trains -- 
        for cart in trains_list:
            x, y = cart.get_pos()
            x -= 1
            y += 1
            position = [ x - self.position[0]*2, y - self.position[1]*2 ]
            tile = map[ str(int(x))+","+str(int(y)) ][0]
            position[1] += tile.get_height()*2
            cart_img = self.texture_pack[ cart.get_name_facing() ] 
            size_x = self.default_tile_size[0] * self.zoom
            size_y = self.default_tile_size[1] * self.zoom*2
            cart_img_scaled = pygame.transform.scale( cart_img, (size_x, size_y) )
            pos_x = (position[0]/2 + y/2 -0.5) * self.default_tile_size[0] * self.zoom
            pos_y = (position[1] + x/2 -3*y/2 -0.5) * self.default_tile_size[1] * self.zoom
            self.screen.blit( cart_img_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2)
                            )

        ...
    
    def render_bg( self, map: Map ):
        self.background.fill((0, 0, 0))
        # -- Define which coords are on screen --
        screen_w_tiles = SCREEN_SIZE[0] / (self.default_tile_size[0] * self.zoom)
        screen_h_tiles = SCREEN_SIZE[1] / (self.default_tile_size[1] * self.zoom)
        x_0 = int(-screen_w_tiles/2 + self.position[0]/2)
        x_1 = int(+screen_w_tiles/2 + self.position[0]/2)

        y_0 = x_0 # TEMP
        y_1 = x_1 # TEMP

        swt = int(screen_w_tiles + 0.99)
        sht = int(screen_w_tiles + 0.99) # TEMP

        # === rendering tiles ===
        for i in range( y_1+sht, y_0-sht-1, -1 ): 
                # -sht/swt needed to load 3 chuncks around center of the screen
            for j in range( x_0-swt, x_1+swt+1 ):
                tile = map[ str(j)+","+str(i) ][0]
                f = i + tile.get_height()
                k = j - tile.get_height()
                # converting isometric coords into coords on screen
                position = [ k - self.position[0]*2 + f - 1,
                             f - self.position[1]*2 + k/2 -3*f/2 - 0.5 ]
                tile_img = self.texture_pack[ tile.get_name() ] 
                size_x = self.default_tile_size[0] * self.zoom
                size_y = self.default_tile_size[1] * self.zoom
                tile_img_scaled = pygame.transform.scale( tile_img, (size_x, size_y) )
                pos_x = (position[0]/2) * self.default_tile_size[0] * self.zoom
                pos_y = position[1] * self.default_tile_size[1] * self.zoom
                if tile.get_height():
                    bg_tile = self.texture_pack[ "default_bg_height" ] # TEMP
                    height = tile.get_height() + 1
                    bg_tile_scaled = pygame.transform.scale( bg_tile, (size_x, height*size_y))
                    dy = self.default_tile_size[1] * self.zoom / 2
                    self.background.blit( bg_tile_scaled, 
                                        (pos_x + 3*SCREEN_SIZE[0]/2,
                                         pos_y + dy + 3*SCREEN_SIZE[1]/2)
                                    )
                self.background.blit( tile_img_scaled, 
                                    (pos_x + 3*SCREEN_SIZE[0]/2,
                                     pos_y + 3*SCREEN_SIZE[1]/2)
                                )
        # === rendering constructions ===
        for i in range( y_0-sht, y_1+sht+1 ): 
                # -sht/swt needed to load 3 chuncks around center of the screen
            for j in range( x_0-swt, x_1+swt+1 ):
                tile = map[ str(j)+","+str(i) ][0]
                const = map[ str(j)+","+str(i) ][1]
                if not const:
                    continue
                displacement = const.get_displacement()
                f = i + tile.get_height() + displacement[0]
                k = j - tile.get_height() + displacement[1]
                # converting isometric coords into coords on screen
                position = [ k - self.position[0]*2 + f - 1,
                             f - self.position[1]*2 + k/2 -3*f/2 - 0.5 ]
                const_img = self.texture_pack[ const.get_name_facing() ] 
                scale = const.get_texture_scale()
                size_x = self.default_tile_size[0] * self.zoom * scale[0]
                size_y = self.default_tile_size[1] * self.zoom * scale[1]
                const_img_scaled = pygame.transform.scale( const_img, (size_x, size_y) )
                pos_x = (position[0]/2) * self.default_tile_size[0] * self.zoom
                pos_y = position[1] * self.default_tile_size[1] * self.zoom
                self.background.blit( const_img_scaled, 
                                    (pos_x + 3*SCREEN_SIZE[0]/2,
                                     pos_y + 3*SCREEN_SIZE[1]/2)
                                )
        self.bg_position = [self.position[0], self.position[1]]
        self.bg_updated = True

    def get_tile( self, screen_coords ):
        scale = self.default_tile_size[1] * self.zoom
        tx = ((3**0.5) / 3) * ((screen_coords[0] - SCREEN_SIZE[0]/2) / scale) + self.position[0]
        ty = ((3**0.5) / 3) * ((screen_coords[0] - SCREEN_SIZE[0]/2) / scale) + self.position[0]
        tx += (screen_coords[1] - SCREEN_SIZE[1]/2) / scale + self.position[1]*2
        ty -= (screen_coords[1] - SCREEN_SIZE[1]/2) / scale + self.position[1]*2

        return str(round(tx)) + "," + str(round(ty))


    def move( self, rel_pos ):
        self.position[0] += rel_pos[0]*self.zoom
        self.position[1] += rel_pos[1]*self.zoom
    def zoom_in( self, amount ):
        if amount > 0:
            self.zoom *= 1.2
        if amount < 0:
            self.zoom /= 1.2
        self.bg_updated = False
