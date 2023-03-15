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
    def get_facing(self):
        return self.facing
    ...

class Rail(Construction):
    come_from: list[str]
    rotate_to: dict[ str: str ]
    texture_scale: [float, float]
    displacement: [float, float]

    def __init__( self, name, facing, c_pack ):
        super().__init__( name, facing )
        self.come_from = c_pack["rail types"][ name ]["come_from"]
        self.rotate_to = c_pack["rail types"][ name ]["rotate_to"]
        self.texture_scale = c_pack["rail types"][ name ]["texture_scale"]
        self.displacement = c_pack["rail types"][ name ]["displacement"]

    def get_name_facing( self):
        return self.name

    def get_come_from( self ):
        return self.come_from
    def get_rotate_to( self ):
        return self.rotate_to
    def get_texture_scale( self ):
        return self.texture_scale
    def get_displacement( self ):
        return self.displacement
            

    ...
    
