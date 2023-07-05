from json import loads
from math import floor, ceil

from item import Item


def load_cart_pack( name ):
    inp = open("cart_packs/" + name + ".json", "r").read()
    cart_pack = loads(inp)
    return cart_pack


class Cart:
    name: str 
    position: [float, float]
    speed: float
    facing: str # N, E, W, S
    inventory: list[ Item ]
    def __init__( self, cart_pack, name, facing, position, height ):
        self.name = name
        self.facing = facing
        self.position = position
        self.height = height 

        self.mass = cart_pack[ "cart types" ][ name ][ "mass" ]
        self.friction = cart_pack[ "cart types" ][ name ][ "friction" ]
        self.power = cart_pack[ "cart types" ][ name ][ "power" ]
        self.texture_scale = cart_pack[ "cart types" ][ name ][ "texture_scale" ]
        self.texture_displacement = cart_pack[ "cart types" ][ name ][ "texture_displacement" ]


        self.speed = 0.1 # TEMP
        self.rotating = False
        self.ramping_up = False
        self.ramping_down = False
        self.stopped = False

    def get_name_facing( self ):
        if self.ramping_up:
            return self.name + "_up_" + self.facing
        if self.ramping_down:
            return self.name + "_down_" + self.facing
        return self.name + "_" + self.facing
    def get_status( self ):
        if self.ramping_up:
            return "up_"
        if self.ramping_down:
            return "down_"
        return ""
    def get_pos( self ):
        return self.position
    def get_height( self ):
        return self.height
    def get_speed( self ):
        return self.speed
    def get_mass( self ):
        return self.mass
    def get_friction( self ):
        return self.friction
    def get_power( self ):
        if self.stopped:
            return 0
        return self.power
    def get_texture_scale( self ):
        return self.texture_scale
    def get_texture_displacement( self ):
        return self.texture_displacement
    def set_speed( self, value ):
        self.speed = value
    def get_stopped( self ):
        return self.stopped
    def set_stopped( self, value ):
        self.stopped = value
    def get_energy( self ):
        return self.speed * self.mass
    
    def get_active_friction( self ):
        if self.stopped:
            return 0
        return self.mass * self.friction * self.speed


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
        neg_facing = negative_list[self.facing]
        if not constr:
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True
        if abs(tile.get_height() - self.height) > 1:
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True
        if tile.get_height() == self.height - 1 and \
                neg_facing not in list(constr.get_ramp_down()):
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True
        if tile.get_height() == self.height + 1 and \
                neg_facing not in list(constr.get_ramp_up()):
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True

        if self.stopped:
            self.stopped = False
            return 
        if self.rotating and rotation_allowed:
            self.facing = self.rotating
            self.position[0] = round(x_1)
            self.position[1] = round(y_1)
            self.rotating = False
            return False
        if (self.ramping_up or self.ramping_down) and rotation_allowed:
            self.position[0] = round(x_1)
            self.position[1] = round(y_1)
            self.height = round(self.height)
            self.ramping_up = False
            self.ramping_down = False
            return False
        

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
        self.stopped = False



class Train(Cart):
    carts: list[ Cart ]
    def __init__( self, carts_list ):
        self.stopped = False
        self.carts = carts_list

    def get_carts( self ):
        return self.carts
    def add_cart( self, cart ):
        self.carts.append(cart)

    def update(self, map):
        self.stopped = False
        
        energies = 0
        sum_mass = 0
        
        for cart in self.carts:
            energies += cart.get_energy() - cart.get_active_friction() + cart.get_power()
            sum_mass += cart.get_mass()
        self.speed = energies / sum_mass

        for cart in self.carts:
            cart.set_speed(self.speed)
            if self.stopped:
                cart.set_stopped( True )
            if cart.update(map):
                self.stopped = True
        if self.stopped:
            for cart in self.carts:
                cart.set_stopped( True )









