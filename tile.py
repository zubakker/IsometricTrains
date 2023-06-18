from perlin_numpy import generate_perlin_noise_2d

from construction import Rail



class Tile:
    height: int
    name: str
    constructions: list

    def __init__( self, name, height ):
        self.name = name
        self.height = height

    def get_name( self ):
        return self.name
    def get_height( self ):
        return self.height
    def change_height( self, change ):
        self.height += change
    def change_name( self, name ):
        self.name = name
    ...


class Map:
    map: dict
    chunck_size: int

    def __init__( self ):
        self.map = dict()
        self.chunck_size = 21

    def __getitem__( self, name ):
        if name not in list(self.map):
            x, y = name.split(",")
            x, y = int(x), int(y)
            self.load_chunck( [x, y] )
        return self.map[name]
    def get_chunck_size( self ):
        return self.chunck_size

    def set_tile( self, pos, tile ):
        self.map[pos][0] = tile 
    def set_construction(self, pos, const ):
        self.map[pos][1] = const

    def generate_chunck( self, position ): 
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
        ...

    def load_chunck( self, position ):
        # if chunck hasn't been saved (it wasn't generated)
        # TEMP
        self.generate_chunck( position )
    def save_chunck( self ): # ...
        ...
    ...

