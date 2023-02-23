class Tile:
    height: int
    name: str

    def __init__( self, name, height ):
        self.name = name
        self.height = height

    def get_name( self ):
        return self.name
    def get_height( self ):
        return self.height
    ...


class Map:
    map: dict

    def __init__( self ):
        self.map = dict()
    def __getitem__( self, name ):
        return self.map[name]

    def generate_chunck( self, position ): # every chunck is 20x20 tiles
        for i in range(-8, 8):
            for j in range(-8, 8):
                # generating flat chunck (temporary)
                tile = Tile( "default_basic_tile", 0 )
                self.map[ str(position[0]*20 + i) + "," + str(position[1]*20 + j) ] = tile 
        ...

    def load_chunck( self, position ):
        # if chunck hasn't been saved (it wasn't generated)
        self.generate_chunck( position )
        ...
    def save_chunck( self ): # ...
        ...
    ...

