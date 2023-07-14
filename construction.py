from json import loads

from math import pi


def load_construction_pack( name ):
    inp = open("construction_packs/" + name + ".json", "r").read()
    construction_pack = loads(inp)
    return construction_pack


class Construction:
    name: str
    facing: str # N, E, W, S, NE, ...

    def __init__( self, name, facing ):
        self.name = name
        self.facing = facing
    def get_name_facing( self ):
        return self.name + "_" + self.facing
    def get_name( self ):
        return self.name
    def get_facing(self):
        return self.facing
    ...

class Rail(Construction):
    come_from: list[str]
    rotate_to: dict[ str: str ]
    texture_scale: [float, float]
    texture_displacement: [float, float]

    def __init__( self, name, facing, constr_pack, type="rail" ):
        self.type = type
        self.directions = "NESW"
        self.directions_rev = {
                "N": 0,
                "E": 1,
                "S": 2,
                "W": 3
                }
        self.rel_directions = ["Front", "Right", "Back", "Left"]
        self.rel_directions_rev = {
                "Front": 0,
                "Right": 1,
                "Back": 2,
                "Left": 3
                }
        super().__init__( name, facing )
        if not name:
            self.constr_pack = constr_pack
            return 
        self.come_from = constr_pack[self.type + " types"][ name ]["come_from"]
        self.rotate_by = constr_pack[self.type + " types"][ name ]["rotate_by"]
        self.rotate_to = constr_pack[self.type + " types"][ name ]["rotate_to"]
        self.required_tiles = constr_pack[self.type + " types"][ name ]["required_tiles"]
        self.texture_scale = constr_pack[self.type + " types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack[self.type + " types"][ name ]["texture_displacement"]
        self.texture_scale = constr_pack[self.type + " types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack[self.type + " types"][ name ]["texture_displacement"]
        self.layer_displacement = constr_pack[self.type + " types"][ name ]["layer_displacement"]
    def get_type(self):
        return self.type

    def get_come_from( self ):
        come_fr = list()
        for dir in self.come_from:
            key = (self.directions_rev[self.facing] + self.rel_directions_rev[dir])%4
            come_fr.append(self.directions[key])
        return come_fr
    def get_rotate_to( self, come_from ):
        key_from = (self.directions_rev[come_from] - self.directions_rev[self.facing]) % 4
        rel_dir_from = self.rel_directions[key_from]
        if rel_dir_from in list(self.rotate_to):
            angle_hor, angle_ver = self.rotate_to[rel_dir_from]
            if angle_hor != 'None':
                angle_hor *= pi/2
            if angle_ver != 'None':
                angle_ver *= pi/2
            return [angle_hor, angle_ver]
        else:
            return ['None', 'None']

    def get_rotate_by( self, come_from ):
        key_from = (self.directions_rev[come_from] - self.directions_rev[self.facing]) % 4
        rel_dir_from = self.rel_directions[key_from]
        if rel_dir_from in list(self.rotate_by):
            angle_hor, angle_ver = self.rotate_by[rel_dir_from]
            return [angle_hor, angle_ver]
        else:
            return [0, 0]
    def get_required_tiles( self ):
        return self.required_tiles
    def get_texture_scale( self ):
        return self.texture_scale
    def get_texture_displacement( self ):
        return self.texture_displacement
    def get_layer_displacement( self ):
        return self.layer_displacement
    

    def output_json( self ):
        output = {
                "constr_type": self.type,
                "constr_name": self.name,
                "constr_facing": self.facing
                }
        return output
    def input_dict( self, input ):
        self.name = input["constr_name"]
        self.facing = input["constr_facing"]
        self.come_from = self.constr_pack[self.type + " types"][ self.name ]["come_from"]
        self.rotate_by = self.constr_pack[self.type + " types"][ self.name ]["rotate_by"]
        self.rotate_to = self.constr_pack[self.type + " types"][ self.name ]["rotate_to"]
        self.required_tiles = self.constr_pack[self.type + " types"][ self.name ]["required_tiles"]
        self.texture_scale = self.constr_pack[self.type + " types"][ self.name ]["texture_scale"]
        self.texture_displacement = self.constr_pack[self.type + " types"][ self.name ]["texture_displacement"]
        self.layer_displacement = self.constr_pack[self.type + " types"][ self.name ]["layer_displacement"]
    def input_json( self, json_txt ):
        input = loads(json_txt)
        self.input_dict(input)


class Station(Rail):
    def __init__( self, name, facing, constr_pack ):
        super().__init__(name, facing, constr_pack, type="station")
        self.status = "stopping"

    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status
    ...
    
