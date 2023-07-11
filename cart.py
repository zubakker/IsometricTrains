from json import loads, dumps
from math import floor, ceil, cos, sin

from math import pi

from item import Item

from constants import GRAVITY


def load_cart_pack( name ):
    inp = open("cart_packs/" + name + ".json", "r").read()
    cart_pack = loads(inp)
    return cart_pack

def save_trains_list( trains_list, path ):
    file = open(path + "/trains.json", 'w+')
    data = []
    for train in trains_list:
        data.append(train.output_json())
    file.write( dumps(data) )
    file.close()

def load_trains_list( path, cart_pack ):
    try:
        file = open(path + "/trains.json", "r").read()
        data = loads(file)

        trains_list = list()
        for input in data:
            a = Train( cart_pack, [] )
            a.input_list(input)
            trains_list.append(a)
        return trains_list
    except FileNotFoundError:
        return []




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

        self.speed = 0.1 # TEMP

        self.rotating = False
        self.ramping_up = False
        self.ramping_down = False
        self.stopped = False
        if self.name == '':
            return

        self.mass = cart_pack[ "cart types" ][ name ][ "mass" ]
        self.friction = cart_pack[ "cart types" ][ name ][ "friction" ]
        self.power = cart_pack[ "cart types" ][ name ][ "power" ]
        self.texture_scale = cart_pack[ "cart types" ][ name ][ "texture_scale" ]
        self.texture_displacement = cart_pack[ "cart types" ][ name ][ "texture_displacement" ]
        
        self.rotation = [{ 
                "E": 0,
                "N": 1,
                "W": 2,
                "S": 3
                }[self.facing] * pi / 2, 0]



    def get_name( self ):
        return self.name
    def get_facing( self ):
        return self.facing
    def get_position( self ):
        return self.position

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
        if self.ramping_up:
            return self.power - self.mass * GRAVITY
        if self.ramping_down:
            return self.power + self.mass * GRAVITY
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
        if self.rotating:
            return 2 * self.mass * self.friction * self.speed
        return self.mass * self.friction * self.speed

    def output_json(self):
        output = {
                "name": self.name,
                "facing": self.facing,
                "position": self.position,
                "stopped": self.stopped,
                "rotating": self.rotating,
                "ramping_up": self.ramping_up,
                "ramping_down": self.ramping_down
                }
        return output
    def input_json(self, json_txt, cart_pack):
        input = loads(json_txt)
        self.name = input["name"]
        self.facing = input["facing"]
        self.position = input["position"]
        self.rotating = input["rotating"]
        self.ramping_up = input["ramping_up"]
        self.ramping_down = input["ramping_down"]
        self.stopped = input["stopped"]
        self.mass = cart_pack[ "cart types" ][ self.name ][ "mass" ]
        self.friction = cart_pack[ "cart types" ][ self.name ][ "friction" ]
        self.power = cart_pack[ "cart types" ][ self.name ][ "power" ]
        self.texture_scale = cart_pack[ "cart types" ][ self.name ][ "texture_scale" ]
        self.texture_displacement = cart_pack[ "cart types" ][ self.name ][ "texture_displacement" ]
    def input_dict(self, inp_dict, cart_pack):
        self.name = inp_dict["name"]
        self.facing = inp_dict["facing"]
        self.position = inp_dict["position"]
        self.rotating = inp_dict["rotating"]
        self.ramping_up = inp_dict["ramping_up"]
        self.ramping_down = inp_dict["ramping_down"]
        self.stopped = inp_dict["stopped"]
        self.mass = cart_pack[ "cart types" ][ self.name ][ "mass" ]
        self.friction = cart_pack[ "cart types" ][ self.name ][ "friction" ]
        self.power = cart_pack[ "cart types" ][ self.name ][ "power" ]
        self.texture_scale = cart_pack[ "cart types" ][ self.name ][ "texture_scale" ]
        self.texture_displacement = cart_pack[ "cart types" ][ self.name ][ "texture_displacement" ]
        
    def update( self, map):
        if self.stopped:
            self.stopped = False
            return 
        negative_dict = {
                            "N": "S",
                            "S": "N",
                            "E": "W",
                            "W": "E"
                        }
        facing_by_angle = "ENWS"
        self.rotating = False
        self.ramping_up = False
        self.ramping_down = False
        x, y = self.position

        x += cos(self.rotation[0]) * self.speed
        y += sin(self.rotation[0]) * self.speed
        # self.height += self.rotation[1] * self.speed

        tile, constr = map[ str(round(x)) + "," + str(round(y)) ]

        if not constr:
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True
        neg_facing = negative_dict[self.facing]
        rel_rotation = constr.rotate( neg_facing )
        if rel_rotation[0] != 0:
            self.rotating = True
        if rel_rotation[1] > 0:
            self.ramping_up = True
        if rel_rotation[1] < 0:
            self.ramping_down = True

        self.rotation[0] += rel_rotation[0] * self.speed
        self.rotation[1] += rel_rotation[1] * self.speed

        if not self.rotating:
            angle = round(2*self.rotation[0]/pi) % 4
            self.rotation[0] = angle*pi / 2
            self.facing = facing_by_angle[angle]

            if -0.0001 <= cos(self.rotation[0]) <= 0.0001:
                x = round(x)
            if -0.0001 <= sin(self.rotation[0]) <= 0.0001:
                y = round(y)

        ramp_up_dir = constr.get_ramp_up()
        ramp_down_dir = constr.get_ramp_down()

        if neg_facing in ramp_up_dir:
            self.ramping_up = True
            self.height += self.speed
        if neg_facing in ramp_down_dir:
            self.ramping_up = True
            self.height += self.speed

        self.position[0] = x
        self.position[1] = y

        self.stopped = False





class Train(Cart):
    carts: list[ Cart ]
    def __init__( self, cart_pack, carts_list, ):
        self.stopped = False
        self.carts = carts_list
        self.cart_pack = cart_pack

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

    def get_stopped(self):
        return self.stopped
    def set_stopped(self, value):
        self.stopped = value

    def output_json(self):
        output = list()
        for cart in self.carts:
            output.append( cart.output_json() )
        return output
    def input_json(self, json_txt):
        input = loads(json_txt)
        for cart_dict in enumerate(input):
            c = Cart( self.cart_pack, '', '', [], 0)
            c.input_dict(cart_dict[-1], self.cart_pack)
            self.carts.append(c)
    def input_list(self, input):
        for cart_dict in enumerate(input):
            c = Cart( self.cart_pack, '', '', [], 0)
            c.input_dict(cart_dict[-1], self.cart_pack)
            self.carts.append(c)













