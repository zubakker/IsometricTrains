class Construction:
    name: str
    facing: str # N, E, W, S, NE, ...

    def __init__( self, name, facing ):
        self.name = name
        self.facing = facing
    def get_name_facing( self ):
        return self.name + "_" + self.facing
    ...

class Rail(Construction):

    def __init__( self, name, facing ):
        super().__init__( name, facing )
    ...
    
