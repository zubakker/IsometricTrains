import os 
import pygame

from math import floor, ceil, log


from tile import Tile, Map

from constants import SCREEN_SIZE, DEFAULT_SAVE_PATH, DEFAULT_TILE_SIZE, MINIMAL_TILE_SIZE


class Camera:
    position: [float, float]
    zoom: float
    texture_pack: dict
    background: pygame.Surface
    screen: pygame.Surface
    default_tile_size: [float, float]
    bg_updated: bool

    def __init__( self, position, zoom, screen, map, constr_pack, cart_pack ):
        self.position = position
        self.zoom = zoom
        self.screen = screen
        self.texture_pack = dict()
        self.load_texture_pack( "default" )

        self.bg_updated = False
        self.background = pygame.Surface( (3*SCREEN_SIZE[0], 3*SCREEN_SIZE[1]) )
        self.bg_position = [0, 0]
        self.cam_height = False 

        chunck_size = map.get_chunck_size()
        map.load_chunck( [position[0]//chunck_size, position[1]//chunck_size],
                DEFAULT_SAVE_PATH, constr_pack, cart_pack )


    def get_tile_list( self ):
        name = self.name
        tile_name  = "texture_packs/tiles/" + name
        return [x[:-4] for x in os.listdir(tile_name)]


    def load_texture_pack( self, name ):
        zoom_steps = ceil(log(DEFAULT_TILE_SIZE[0] / MINIMAL_TILE_SIZE[0], 2))
        self.name = name
        for step in range(zoom_steps+1):
            self.texture_pack[ 2**step ] = dict()
        
        tile_name  = "texture_packs/tiles/" + name
        constr_name = "texture_packs/constructions/" + name
        cart_name  = "texture_packs/carts/" + name
        button_name  = "texture_packs/buttons/" + name
        tile_textures = os.listdir( tile_name )
        constr_textures = os.listdir( constr_name )
        cart_textures = os.listdir( cart_name )
        button_textures = os.listdir( button_name )
        texture_dirs = { 
                    tile_name:  tile_textures,
                    constr_name:    constr_textures,
                    cart_name:  cart_textures,
                    button_name:    button_textures
                }
        for dir, textures in texture_dirs.items():
            for texture in textures:
                self.texture_pack[1][ texture[:-4] ] = pygame.image.load(dir  +"/"+ texture)

        for key, image in self.texture_pack[1].items():
            for step in range(1, zoom_steps+1):
                size_x = DEFAULT_TILE_SIZE[0] // 2**(step-1)
                size_y = DEFAULT_TILE_SIZE[1] // 2**(step-1)
                scaled_img = pygame.transform.scale( image, (size_x, size_y) )
                self.texture_pack[ 2**step ][key] = scaled_img
    def get_texture( self, name, ignore_zoom=False):
        zoom_step = -floor(log(self.zoom, 2))
        if ignore_zoom:
            zoom_step = 0
        if name not in list(self.texture_pack[2**zoom_step]):
            print('Texture not found:', name)
            return self.texture_pack[2**zoom_step]['error']

        return self.texture_pack[2**zoom_step][name]
    def get_position( self):
        return self.position

    def render( self, map, trains_list, cart_pack ):
        if not self.bg_updated:
            self.render_bg( map )

        dx = self.position[0] - self.bg_position[0]
        dy = self.position[1] - self.bg_position[1]
        posx = -SCREEN_SIZE[0] - DEFAULT_TILE_SIZE[0]*dx*self.zoom
        posy = -SCREEN_SIZE[1] - DEFAULT_TILE_SIZE[1]*dy*self.zoom
        if posx > 0 or posy > 0:
            self.render_bg( map )
        if posx + SCREEN_SIZE[0]*2 < 0 or posy + SCREEN_SIZE[1]*2 < 0:
            self.render_bg( map )
        self.screen.blit( self.background, (posx, posy) )

        # -- Rendering trains -- 
        for train in trains_list:
            rendering_list = list()
            for cart in train.get_carts():
                x, y = cart.get_pos()
                x -= 1
                y += 1
                angles_list = cart_pack["cart rotations"]
                cart_angle = cart.get_rotation()
                min_delta = abs(angles_list[0][0] - cart_angle[0]) + abs(angles_list[0][1] - cart_angle[1])
                min_angle = angles_list[0]
                for angle in angles_list:
                    delta = abs(angle[0] - cart_angle[0]) + abs(angle[1] - cart_angle[1])
                    if delta < min_delta:
                        min_angle = angle
                        min_delta = delta
                angle = str(round(min_angle[0],3))+","+str(round(min_angle[1],3))

                    


                texture_displacement_dict = cart.get_texture_displacement()
                if angle in texture_displacement_dict:
                    texture_displacement = texture_displacement_dict[ angle ]
                else:
                    texture_displacement = texture_displacement_dict["ALL"]
                k = x - cart.get_height() + texture_displacement[0] 
                f = y + cart.get_height() + texture_displacement[1] 
                # converting isometric coords into coords on screen
                position = [ k - self.position[0]*2 + f - 1,
                             f - self.position[1] + k/2 -3*f/2 - 0.5 ]
                cart_img = self.get_texture(cart.get_name()+"_"+angle)
                scale_dict = cart.get_texture_scale()
                if angle in scale_dict.keys():
                    scale = scale_dict[ angle ]
                else:
                    scale = scale_dict["ALL"]
                size_x = DEFAULT_TILE_SIZE[0] * self.zoom * scale[0]
                size_y = DEFAULT_TILE_SIZE[1] * self.zoom*2 * scale[1]
                cart_height = cart.get_height()
                cart_img_scaled = pygame.transform.scale( cart_img, (size_x, size_y) )
                pos_x = (position[0]/2) * DEFAULT_TILE_SIZE[0] * self.zoom
                pos_y = position[1] * DEFAULT_TILE_SIZE[1] * self.zoom
                rendering_list.append([pos_x, pos_y, cart_img_scaled, cart.get_pos(), cart_height])
            for cart_props in sorted(rendering_list, key=lambda x: x[1]):
                pos_x, pos_y, cart_img_scaled, pos, cart_height = cart_props
                self.screen.blit( cart_img_scaled, 
                                        (pos_x + SCREEN_SIZE[0]/2,
                                         pos_y + SCREEN_SIZE[1]/2)
                                    )
            for cart_props in sorted(rendering_list, key=lambda x: x[1]):
                pos_x, pos_y, cart_img_scaled, pos, cart_height = cart_props
                x, y = pos
                x, y = int(x), int(y)
                if map[ str(x+1) +","+ str(y) ][0].get_height() > cart_height:
                    self.render_tile(map, (x+1, y))
                if map[ str(x) +","+ str(y-1) ][0].get_height() > cart_height:
                    self.render_tile(map, (x, y-1))
                for i in range(1, map.get_chunck_size()):
                    if map[ str(x+i) +","+ str(y-i) ][0].get_height() >= i:
                        self.render_tile(map, (x+i, y-i))
                    if map[ str(x+i+1) +","+ str(y-i) ][0].get_height() >= i:
                        self.render_tile(map, (x+i+1, y-i))
                    if map[ str(x+i) +","+ str(y-i-1) ][0].get_height() >= i:
                        self.render_tile(map, (x+i, y-i-1))


        ...
    def render_tile(self, map, position):
        j, i = position
        tile = map[ str(j)+","+str(i) ][0]
        tile_e = map[ str(j+1)+","+str(i) ][0]
        tile_s = map[ str(j)+","+str(i-1) ][0]

        height = tile.get_height()
        height_e = tile_e.get_height()
        height_s = tile_s.get_height()
        tile_img = self.get_texture(tile.get_name())
        if height > self.cam_height:
            height = self.cam_height
            tile_img = self.get_texture(tile.get_type()+"_black_nb") # TEMP
        if height_e > self.cam_height:
            height_e = self.cam_height
        if height_s > self.cam_height:
            height_s = self.cam_height
        f = i + height
        k = j - height
        # converting isometric coords into coords on screen
        position = [ k - self.position[0]*2 + f - 1,
                     f - self.position[1] + k/2 -3*f/2 - 0.5 ]
        size_x = DEFAULT_TILE_SIZE[0] * self.zoom
        size_y = DEFAULT_TILE_SIZE[1] * self.zoom
        tile_img_scaled = pygame.transform.scale( tile_img, (size_x, size_y) )
        pos_x = (position[0]/2) * DEFAULT_TILE_SIZE[0] * self.zoom
        pos_y = position[1] * DEFAULT_TILE_SIZE[1] * self.zoom

        if height_s < height and height_e < height:
            # render tile and walls 
            wall_height = height - max(height_e, height_s)
            bg_height = self.get_texture("default_bg_height_nb") # TEMP
            bg_wall = self.get_texture("default_bg_wall_nb") # TEMP
            bg_wall_scaled = pygame.transform.scale( bg_wall, (size_x, 2*size_y))
            bg_height_scaled = pygame.transform.scale( bg_height, 
                    (size_x, size_y*(wall_height-0.5)))
            dy = DEFAULT_TILE_SIZE[1] * self.zoom / 2

            self.screen.blit( bg_wall_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2 +size_y*(wall_height-1))
                            )
            self.screen.blit( bg_height_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2 + size_y*0.5)
                            )
            height -= wall_height
        if height_e < height:
            # render tile and right wall
            bg_height = self.get_texture("default_bg_height_right_nb") # TEMP
            bg_wall = self.get_texture("default_bg_wall_right_nb") # TEMP
            bg_wall_scaled = pygame.transform.scale( bg_wall, (size_x, 2*size_y))
            bg_height_scaled = pygame.transform.scale( bg_height, 
                    (size_x, size_y*(height-0.5)))
            dy = DEFAULT_TILE_SIZE[1] * self.zoom / 2

            self.screen.blit( bg_wall_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2 +size_y*(height-1))
                            )
            self.screen.blit( bg_height_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2 + size_y*0.5)
                            )
        elif height_s < height:
            # render tile and left wall
            bg_height = self.get_texture("default_bg_height_left_nb") # TEMP
            bg_wall = self.get_texture("default_bg_wall_left_nb") # TEMP
            bg_wall_scaled = pygame.transform.scale( bg_wall, (size_x, 2*size_y))
            bg_height_scaled = pygame.transform.scale( bg_height, 
                    (size_x, size_y*(height-0.5)))
            dy = DEFAULT_TILE_SIZE[1] * self.zoom / 2

            self.screen.blit( bg_wall_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2 +size_y*(height-1))
                            )
            self.screen.blit( bg_height_scaled, 
                                (pos_x + SCREEN_SIZE[0]/2,
                                 pos_y + SCREEN_SIZE[1]/2 + size_y*0.5)
                            )

        self.screen.blit( tile_img_scaled, 
                            (pos_x + SCREEN_SIZE[0]/2,
                             pos_y + SCREEN_SIZE[1]/2)
                        )
        # === rendering constructions ===
        const = map[ str(j)+","+str(i) ][1]
        if not const:
            return
        texture_displacement_dict = const.get_texture_displacement()
        if "NESW" in texture_displacement_dict:
            texture_displacement = texture_displacement_dict["NESW"]
        else:
            texture_displacement = texture_displacement_dict[ const.get_facing() ]
        if tile.get_height() > self.cam_height:
            return
        f = i + height + texture_displacement[1] 
        k = j - height + texture_displacement[0] 
        position = [ k - self.position[0]*2 + f - 1,
                     f - self.position[1] + k/2 -3*f/2 - 0.5 ]
        pos_x = (position[0]/2) * DEFAULT_TILE_SIZE[0] * self.zoom
        pos_y = position[1] * DEFAULT_TILE_SIZE[1] * self.zoom
        const_img = self.get_texture(const.get_name_facing())
        scale_dict = const.get_texture_scale()
        if "NESW" in scale_dict.keys():
            scale = scale_dict["NESW"]
        else:
            scale = scale_dict[ const.get_facing() ]
        size_x = DEFAULT_TILE_SIZE[0] * self.zoom * scale[0]
        size_y = DEFAULT_TILE_SIZE[1] * self.zoom * scale[1]
        const_img_scaled = pygame.transform.scale( const_img, (size_x, size_y) )
        self.screen.blit( const_img_scaled, 
                            (pos_x + SCREEN_SIZE[0]/2,
                             pos_y + SCREEN_SIZE[1]/2)
                        )
 
    
    def render_bg( self, map: Map ):
        self.background.fill((0,0,0))
        # -- Define which coords are on screen --
        screen_w_tiles = SCREEN_SIZE[0] / (DEFAULT_TILE_SIZE[0] * self.zoom)
        screen_h_tiles = SCREEN_SIZE[1] / (DEFAULT_TILE_SIZE[1] * self.zoom)
        x_0 = int(-screen_w_tiles/2 + self.position[0]/2)
        x_1 = int(+screen_w_tiles/2 + self.position[0]/2)

        y_0 = x_0 # TEMP
        y_1 = x_1 # TEMP

        swt = int(screen_w_tiles + 0.99)
        sht = int(screen_w_tiles + 0.99) # TEMP

        render_queue = list()

        for i in range( y_1+sht, y_0-sht-1, -1 ): 


            # -sht/swt needed to load 3 chuncks around center of the screen
            for j in range( x_0-swt, x_1+swt+1 ):

                # === rendering tiles ===
                tile = map[ str(j)+","+str(i) ][0]
                height = tile.get_height()
                tile_img = self.get_texture(tile.get_name())
                if height > self.cam_height:
                    height = self.cam_height
                    tile_img = self.get_texture(tile.get_type() + "_black_nb") # TEMP
                f = i + height
                k = j - height
                # converting isometric coords into coords on screen
                position = [ k - self.position[0]*2 + f - 1,
                             f - self.position[1] + k/2 -3*f/2 - 0.5 ]
                size_x = DEFAULT_TILE_SIZE[0] * self.zoom
                size_y = DEFAULT_TILE_SIZE[1] * self.zoom
                tile_img_scaled = pygame.transform.scale( tile_img, (size_x, size_y) )
                pos_x = (position[0]/2) * DEFAULT_TILE_SIZE[0] * self.zoom
                pos_y = position[1] * DEFAULT_TILE_SIZE[1] * self.zoom

                if height:
                    bg_height = self.get_texture("default_bg_height_nb") # TEMP
                    bg_wall = self.get_texture("default_bg_wall_nb") # TEMP
                    bg_wall_scaled = pygame.transform.scale( bg_wall, (size_x, 2*size_y))
                    bg_height_scaled = pygame.transform.scale( bg_height, 
                            (size_x, size_y*(height-1)*1.5))
                    dy = DEFAULT_TILE_SIZE[1] * self.zoom / 2

                    self.background.blit( bg_wall_scaled, 
                                        (pos_x + 3*SCREEN_SIZE[0]/2,
                                         pos_y + 3*SCREEN_SIZE[1]/2 +size_y*(height-1))
                                    )
                    self.background.blit( bg_height_scaled, 
                                        (pos_x + 3*SCREEN_SIZE[0]/2,
                                         pos_y + 3*SCREEN_SIZE[1]/2 + size_y*0.5)
                                    )
                self.background.blit( tile_img_scaled, 
                                    (pos_x + 3*SCREEN_SIZE[0]/2,
                                     pos_y + 3*SCREEN_SIZE[1]/2)
                                )
                # === rendering constructions ===
                for t, construction in enumerate(render_queue):
                    if construction[0] == [j,i]:
                        pos_x, pos_y, const_img_scaled = construction[1]
                        self.background.blit( const_img_scaled, 
                                            (pos_x + 3*SCREEN_SIZE[0]/2,
                                             pos_y + 3*SCREEN_SIZE[1]/2)
                                        )
                        render_queue.pop(t)
                const = map[ str(j)+","+str(i) ][1]
                if not const:
                    continue
                texture_displacement_dict = const.get_texture_displacement()
                if "NESW" in texture_displacement_dict:
                    texture_displacement = texture_displacement_dict["NESW"]
                else:
                    texture_displacement = texture_displacement_dict[ const.get_facing() ]
                if tile.get_height() > self.cam_height:
                    continue
                f = i + tile.get_height() + texture_displacement[0]
                k = j - tile.get_height() + texture_displacement[1]
                # converting isometric coords into coords on screen
                position = [ k - self.position[0]*2 + f - 1,
                             f - self.position[1] + k/2 -3*f/2 - 0.5 ]
                const_img = self.get_texture(const.get_name_facing())
                scale_dict = const.get_texture_scale()
                if "NESW" in scale_dict.keys():
                    scale = scale_dict["NESW"]
                else:
                    scale = scale_dict[ const.get_facing() ]
                size_x = DEFAULT_TILE_SIZE[0] * self.zoom * scale[0]
                size_y = DEFAULT_TILE_SIZE[1] * self.zoom * scale[1]
                const_img_scaled = pygame.transform.scale( const_img, (size_x, size_y) )
                pos_x = (position[0]/2) * DEFAULT_TILE_SIZE[0] * self.zoom
                pos_y = position[1] * DEFAULT_TILE_SIZE[1] * self.zoom
                layer_dict = const.get_layer_displacement()
                if "NESW" in layer_dict.keys():
                    layer = layer_dict["NESW"]
                else:
                    layer = layer_dict[ const.get_facing() ]

                if layer != [0,0]:
                    layer_x, layer_y = layer
                    render_queue.append( [[layer_x+j, -layer_y+i], [pos_x, pos_y, const_img_scaled]] )
                    continue
                    
                self.background.blit( const_img_scaled, 
                                    (pos_x + 3*SCREEN_SIZE[0]/2,
                                     pos_y + 3*SCREEN_SIZE[1]/2)
                                )
        self.bg_position = [self.position[0], self.position[1]]
        self.bg_updated = True

    def get_tile( self, screen_coords, map ):
        scale = DEFAULT_TILE_SIZE[1] * self.zoom
        tx = ((3**0.5) / 3) * ((screen_coords[0] - SCREEN_SIZE[0]/2) / scale) + self.position[0]
        ty = ((3**0.5) / 3) * ((screen_coords[0] - SCREEN_SIZE[0]/2) / scale) + self.position[0]
        tx += (screen_coords[1] - SCREEN_SIZE[1]/2) / scale + self.position[1]
        ty -= (screen_coords[1] - SCREEN_SIZE[1]/2) / scale + self.position[1]
        x = round(tx)
        y = round(ty)
            
        for i in range( map.get_chunck_size(), -1, -1 ):
            if min(map[ str(x+i) +","+ str(y-i) ][0].get_height(), self.cam_height) == i:
                return str(x+i) +"," + str(y-i)




    def move( self, rel_pos ):
        self.position[0] += rel_pos[0]/self.zoom
        self.position[1] += rel_pos[1]/self.zoom
    def move_vert( self, rel_pos, map):
        if not self.cam_height and self.cam_height != 0:
            self.cam_height = 10 # TEMP
        self.cam_height += rel_pos
        self.render_bg( map )

    def zoom_in( self, amount ):
        if amount > 0:
            self.zoom *= 1.2
            if self.zoom > 1:
                self.zoom = 1
        if amount < 0:
            self.zoom /= 1.2
            if self.zoom < 1/ max(list(self.texture_pack)):
                self.zoom = 1/ max(list(self.texture_pack))
        self.bg_updated = False
