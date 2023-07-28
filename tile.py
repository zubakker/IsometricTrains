from json import dumps, loads
from random import randint

from perlin_numpy import generate_perlin_noise_2d

from construction import Rail, Station, Factory

from constants import CHUNCK_SIZE, DEFAULT_SAVE_PATH


class Tile:
    height: int
    name: str
    constructions: list

    def __init__( self, name, height ):
        self.name = name + str(height%5)
        self.type = name
        self.height = height

    def get_name( self ):
        return self.name
    def get_type(self):
        return self.type
    def get_height( self ):
        return self.height
    def change_height( self, change ):
        self.height += change
    def change_name( self, name ):
        self.name = name

    def output_json(self):
        output = {
                "tile_name": self.name,
                "tile_type": self.type,
                "tile_height":   self.height
                }
        return output
    def input_json(self, json_txt):
        input = loads(json_txt)
        self.name = input["tile_name"]
        self.type = input["tile_type"]
        self.height = input["tile_height"]
    def input_dict(self, input):
        self.name = input["tile_name"]
        self.type = input["tile_type"]
        self.height = input["tile_height"]


class Map:
    map: dict
    chunck_size: int

    def __init__( self, constr_pack, cart_pack ):
        self.map = dict()
        self.chunck_size = CHUNCK_SIZE
        self.constr_pack = constr_pack
        self.cart_pack = cart_pack
        self.factory_list = list()

    def __getitem__( self, name ):
        if name not in list(self.map):
            x, y = name.split(",")
            x, y = int(x), int(y)
            self.load_chunck( [x, y], DEFAULT_SAVE_PATH, self.constr_pack, self.cart_pack )
        return self.map[name]
    def get_chunck_size( self ):
        return self.chunck_size

    def set_tile( self, pos, tile ):
        if pos not in list(self.map):
            self.map[pos] = [tile, None]
        else:
            self.map[pos][0] = tile 
    def set_construction(self, pos, constr):
        if not constr:
            return False
        x, y = pos.split(',')
        x, y = int(x), int(y)
        height = self.map[pos][0].get_height()
        required_tiles_dict = constr.get_required_tiles()
        facing = constr.get_facing()
        if "NESW" in required_tiles_dict:
            required_tiles = required_tiles_dict["NESW"]
        else:
            required_tiles = required_tiles_dict[facing]
        for tile in required_tiles:
            test_pos = str(x + tile[0])+","+str(y + tile[1])
            if self.map[test_pos][0].get_height() != height:
                return False
            data = constr.output_json()
            data["constr_name"] += "_nr"
            if constr.get_name() in list(self.constr_pack["rail types"]):
                nr_constr = Rail('','', self.constr_pack)
            elif constr.get_name() in list(self.constr_pack["station types"]):
                nr_constr = Station('','', self.constr_pack)
            nr_constr.input_dict(data)

            if test_pos not in list(self.map):
                self.map[test_pos] = [None, nr_constr]
            else:
                self.map[test_pos][1] = nr_constr



        if pos not in list(self.map):
            self.map[pos] = [None, constr]
        else:
            self.map[pos][1] = constr
        return True

    def generate_chunck( self, position, constr_pack ): 
        cs = self.chunck_size
        chunck_center = [0, 0] 
        chunck_center[0] = (position[0] + cs//2) // cs
        chunck_center[1] = (position[1] + cs//2) // cs

        noise = generate_perlin_noise_2d((cs, cs), (3, 3))
        for i in range(-cs//2, cs//2 + 1):
            for j in range(-cs//2, cs//2 + 1):
                # generating noise-based chunck
                height = abs(noise[i, j]*5)
                tile = Tile( "default_basic_tile", int(height) )
                self.map[ str(chunck_center[0]*cs + i) + "," 
                        + str(chunck_center[1]*cs + j) ] = [tile , None]
        # TEMP starts:
        factory_x = randint(-cs//2, cs//2)
        factory_y = randint(-cs//2, cs//2)
        factory = Factory("default_factory", "N", constr_pack)
        self.map[ str(chunck_center[0]*cs + factory_x) + ","
                  + str(chunck_center[1]*cs + factory_y)][1] = factory
        mines_x = randint(-cs//2, cs//2)
        mines_y = randint(-cs//2, cs//2)
        mines = Factory("default_mines", "N", constr_pack)
        self.map[ str(chunck_center[0]*cs + mines_x) + ","
                  + str(chunck_center[1]*cs + mines_y)][1] = mines
        self.factory_list.append(factory)
        self.factory_list.append(mines)
        # :TEMP ends

    def load_chunck( self, position, path, constr_pack, cart_pack ):
        cs = self.chunck_size
        chunck_center = [0, 0] 
        chunck_center[0] = str((position[0] + cs//2) // cs)
        chunck_center[1] = str((position[1] + cs//2) // cs)
        chunck_pos = ",".join(chunck_center)
        try:
            data = loads(open(path + "/" + chunck_pos + ".json", "r").read())
            for key, value in data.items():
                tile = Tile('',0)
                tile.input_dict(value)
                if 'constr_name' in list(value):
                    if value["constr_type"] == "station":
                        constr = Station('','', constr_pack)
                    if value["constr_type"] == "factory":
                        constr = Factory('','', constr_pack)
                        self.factory_list.append(constr)
                    else:
                        constr = Rail('', '', constr_pack)
                    constr.input_dict(value)
                else:
                    constr = None
                self.set_tile( key, tile )
                self.set_construction( key, constr )
                    
        except FileNotFoundError:
        # if chunck hasn't been saved (it wasn't generated)
            self.generate_chunck( position, constr_pack )
    def save_chunck( self, position, path, trains_list ): # ...
        cs = self.chunck_size
        chunck_center = [0, 0] 
        chunck_center[0] = str((position[0] + cs//2) // cs)
        chunck_center[1] = str((position[1] + cs//2) // cs)
        chunck_pos = ",".join(chunck_center)
        data = dict()
        for key, a in self.map.items():
            tile, construction = a
            data[key] = tile.output_json()
            if construction:
                data[key].update( construction.output_json() )
            
        fout = open(path + "/" + chunck_pos + ".json", "w+")
        fout.write(dumps(data))
        fout.close()

    def update_factories(self):
        for factory in self.factory_list:
            factory.update()
