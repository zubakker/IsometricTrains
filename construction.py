from json import loads


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

    def __init__( self, name, facing, constr_pack ):
        self.directions = "NESW"
        self.directions_rev = {
                "N": 0,
                "E": 1,
                "S": 2,
                "W": 3
                }
        self.rel_directions_rev = {
                "Front": 0,
                "Right": 1,
                "Back": 2,
                "Left": 3
                }
        super().__init__( name, facing )
        self.come_from = constr_pack["rail types"][ name ]["come_from"]
        self.rotate_to = constr_pack["rail types"][ name ]["rotate_to"]
        self.ramp_up = constr_pack["rail types"][ name ]["ramp_up"]
        self.ramp_down = constr_pack["rail types"][ name ]["ramp_down"]
        self.texture_scale = constr_pack["rail types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack["rail types"][ name ]["texture_displacement"]

    def get_come_from( self ):
        come_fr = list()
        for dir in self.come_from:
            key = (self.directions_rev[self.facing] + self.rel_directions_rev[dir])%4
            come_fr.append(self.directions[key])
        return come_fr
    def get_rotate_to( self ):
        rotate_t = dict()
        for dir_from, dir_to in self.rotate_to.items():
            key_from = (self.directions_rev[self.facing] + self.rel_directions_rev[dir_from])%4
            key_to = (self.directions_rev[self.facing] + self.rel_directions_rev[dir_to])%4
            rotate_t[self.directions[key_from]] = self.directions[key_to]
        return rotate_t
    def get_ramp_up( self ):
        ramp_u = dict()
        for dir_from, dir_to in self.ramp_up.items():
            key_from = (self.directions_rev[self.facing] + self.rel_directions_rev[dir_from])%4
            key_to = (self.directions_rev[self.facing] + self.rel_directions_rev[dir_to])%4
            ramp_u[self.directions[key_from]] = self.directions[key_to]
        return ramp_u
    def get_ramp_down( self ):
        ramp_d = dict()
        for dir_from, dir_to in self.ramp_down.items():
            key_from = (self.directions_rev[self.facing] + self.rel_directions_rev[dir_from])%4
            key_to = (self.directions_rev[self.facing] + self.rel_directions_rev[dir_to])%4
            ramp_d[self.directions[key_from]] = self.directions[key_to]
        return ramp_d
    def get_texture_scale( self ):
        return self.texture_scale
    def get_texture_displacement( self ):
        return self.texture_displacement
            

    ...
    
