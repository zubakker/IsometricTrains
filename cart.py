from math import floor, ceil


from item import Item


class Cart:
    name: str 
    position: [float, float]
    speed: float
    facing: str # N, E, W, S, NE, ...
    inventory: list[ Item ]
    def __init__( self, name, facing, position ):
        self.name = name
        self.facing = facing
        self.position = position
        self.speed = 0.03 # TEMP
        self.rotating = False

    def get_name_facing( self ):
        return self.name + "_" + self.facing
    def get_pos( self ):
        return self.position

    def update( self, map ): 
        negative_list = {
                            "N": "S",
                            "S": "N",
                            "E": "W",
                            "W": "E"
                        }
        x, y = self.position
        x_1, y_1 = self.position

        if self.facing == "N":
            y = ceil( self.position[1] + self.speed )
            y_1 = self.position[1]+self.speed
            rotation_allowed = ceil( y_1 + self.speed ) > ceil(y_1)
        if self.facing == "S":
            y = floor( self.position[1] - self.speed )
            y_1 = self.position[1]-self.speed
            rotation_allowed = ceil( y_1 - self.speed ) < ceil(y_1)
        if self.facing == "E":
            x = ceil( self.position[0] + self.speed )
            x_1 = self.position[0]+self.speed
            rotation_allowed = ceil( x_1 + self.speed ) > ceil(x_1)
        if self.facing == "W":
            x = floor( self.position[0] - self.speed )
            x_1 = self.position[0]-self.speed
            rotation_allowed = ceil( x_1 - self.speed ) < ceil(x_1)

        constr = map[ str(x) + "," + str(y) ][1]

        if not constr:
            return 
        constr_facing = constr.get_facing()
        if self.rotating and rotation_allowed:
            self.facing = self.rotating
            self.position[0] = round(x_1)
            self.position[1] = round(y_1)
            self.rotating = False
            return
        neg_facing = negative_list[self.facing]

        if neg_facing in constr.get_come_from():
            self.position = [x_1, y_1]
            rotation_dict = constr.get_rotate_to()
            if neg_facing in list(rotation_dict):
                self.rotating = rotation_dict[ neg_facing ]


class Train:
    carts: list[ Cart ]
    ...
