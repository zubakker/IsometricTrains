from math import floor, ceil


from item import Item


class Cart:
    name: str 
    position: [float, float]
    speed: float
    facing: str # N, E, W, S, NE, ...
    inventory: list[ Item ]
    def __init__( self, name, facing, position, height ):
        self.name = name
        self.facing = facing
        self.position = position
        self.height = height 
        self.speed = 0.03 # TEMP
        self.rotating = False
        self.ramping_up = False
        self.ramping_down = False

    def get_name_facing( self ):
        if self.ramping_up:
            return self.name + "_up_" + self.facing
        if self.ramping_down:
            return self.name + "_down_" + self.facing
        return self.name + "_" + self.facing
    def get_pos( self ):
        return self.position
    def get_height( self ):
        return self.height

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

        if self.ramping_up in ["N","S"]:
            self.height += self.speed
        if self.ramping_up in ["W","E"]:
            self.height += self.speed
        if self.ramping_down in ["N","S"]:
            self.height -= self.speed
        if self.ramping_down in ["W","E"]:
            self.height -= self.speed


        tile, constr = map[ str(x) + "," + str(y) ]

        if not constr:
            # either goes off the rail or stops completely
            # TEMP does nothing
            return 
        if self.rotating and rotation_allowed:
            self.facing = self.rotating
            self.position[0] = round(x_1)
            self.position[1] = round(y_1)
            self.rotating = False
            return
        if (self.ramping_up or self.ramping_down) and rotation_allowed:
            self.position[0] = round(x_1)
            self.position[1] = round(y_1)
            self.height = round(self.height)
            self.ramping_up = False
            self.ramping_down = False
            return
        
        neg_facing = negative_list[self.facing]
        if abs(tile.get_height() - self.height) > 1:
            # either goes off the rail or stops completely
            # TEMP does nothing
            return
        if tile.get_height() == self.height - 1 and \
                neg_facing not in list(constr.get_ramp_down()):
            # either goes off the rail or stops completely
            # TEMP does nothing
            return
        if tile.get_height() == self.height + 1 and \
                neg_facing not in list(constr.get_ramp_up()):
            # either goes off the rail or stops completely
            # TEMP does nothing
            return

        if neg_facing in constr.get_come_from():
            self.position = [x_1, y_1]
            rotation_dict = constr.get_rotate_to()
            ramp_up_dict = constr.get_ramp_up()
            ramp_down_dict = constr.get_ramp_down()
            if neg_facing in list(rotation_dict):
                self.rotating = rotation_dict[ neg_facing ]
            if neg_facing in list(ramp_up_dict):
                self.ramping_up = ramp_up_dict[ neg_facing ]
            if neg_facing in list(ramp_down_dict):
                self.ramping_down = ramp_down_dict[ neg_facing ]



class Train:
    carts: list[ Cart ]
    ...
