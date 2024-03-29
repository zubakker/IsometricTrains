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

        self.stopped = False
        self.stopping = False
        if self.name == '':
            return

        self.mass = cart_pack[ "cart types" ][ name ][ "mass" ]
        self.friction = cart_pack[ "cart types" ][ name ][ "friction" ]
        self.power = cart_pack[ "cart types" ][ name ][ "power" ]
        self.inventory_space = cart_pack[ "cart types" ][ name ][ "inventory_space" ]
        self.texture_scale = cart_pack[ "cart types" ][ name ][ "texture_scale" ]
        self.texture_displacement = cart_pack[ "cart types" ][ name ][ "texture_displacement" ]
        self.inventory = list()
        
        self.rotation = [{ 
                "N": 0,
                "E": 1,
                "S": 2,
                "W": -1
                }[self.facing] * pi / 2, 0]



    def get_name( self ):
        return self.name
    def get_facing( self ):
        return self.facing
    def get_position( self ):
        return self.position

    def get_name_facing( self ):
        return self.name + "_" + self.facing
    def get_status( self ):
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
        return self.power - sin(self.rotation[1])*self.mass * GRAVITY
    def get_inventory_space(self):
        return self.inventory_space
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
    def get_rotation( self):
        return [self.rotation[0], self.rotation[1]]
    def set_stopping(self, value):
        if value == "Toggle":
            self.stopping = not self.stopping
            self.stopped = False
            return
        self.stopping = value
    
    def get_active_friction( self ):
        if self.stopped:
            return 0
        return self.mass * self.friction * self.speed

    def get_tile(self):
        return str(round(self.position[0]))+","+str(round(self.position[1]))

    def output_json(self):
        output = {
                "name": self.name,
                "facing": self.facing,
                "position": self.position,
                "stopped": self.stopped,
                "inventory": self.inventory,
                "rotation": self.rotation
                }
        return output
    def input_dict(self, inp_dict, cart_pack):
        self.name = inp_dict["name"]
        self.facing = inp_dict["facing"]
        self.position = inp_dict["position"]
        self.rotation = inp_dict["rotation"]
        self.stopped = inp_dict["stopped"]
        self.inventory = inp_dict["inventory"]
        self.mass = cart_pack[ "cart types" ][ self.name ][ "mass" ]
        self.friction = cart_pack[ "cart types" ][ self.name ][ "friction" ]
        self.power = cart_pack[ "cart types" ][ self.name ][ "power" ]
        self.inventory_space = cart_pack[ "cart types" ][ self.name ][ "inventory_space" ]
        self.texture_scale = cart_pack[ "cart types" ][ self.name ][ "texture_scale" ]
        self.texture_displacement = cart_pack[ "cart types" ][ self.name ][ "texture_displacement" ]
    def input_json(self, json_txt, cart_pack):
        input = loads(json_txt)
        self.input_dict(input)
        
    def update(self, map, dont_move=False):
        negative_dict = {
                            "N": "S",
                            "S": "N",
                            "E": "W",
                            "W": "E"
                        }
        facing_by_angle = "NWSE"
        self.rotating = False
        self.ramping_up = False
        self.ramping_down = False
        x, y = self.position
        tile, constr = map[ str(round(x)) + "," + str(round(y)) ]


        if not constr:
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True
        if constr.get_type() == "station" and \
                abs(self.position[0] - round(self.position[0])) < self.speed and \
                abs(self.position[1] - round(self.position[1])) < self.speed:
            # and \
            # constr.get_status() == "stopping":
            for i, item in enumerate(self.inventory):
                result = constr.load_item(item)
                if result:
                    # if at least one item in the inventory can be loaded
                    # into station cart stops until it cannot be unloaded anymore
                    if type(result) != bool:
                        self.inventory.pop(i)
                    self.position[0] = round(x)
                    self.position[1] = round(y)
                    self.stopped = True
                    return True
            if len(self.inventory) < self.inventory_space:
                item = constr.unload_item()
                if item:
                    # cart stops if cart can be loaded and station can unload items
                    self.position[0] = round(x)
                    self.position[1] = round(y)
                    if not type(item) == bool:
                        self.inventory.append(item)
                    self.stopped = True
                    return True
        if dont_move:
            return False
            

        x -= sin(pi*self.rotation[0]/2) * self.speed 
        y += cos(pi*self.rotation[0]/2) * self.speed 
        self.height += sin(pi*self.rotation[1]/2) * self.speed
        if self.stopping and abs(round(x) - x) < self.speed and \
                abs(round(y) - y) < self.speed:
            # either goes off the rail or stops completely
            # TEMP does nothing
            self.stopped = True
            return True

        neg_facing = negative_dict[self.facing]
        rel_rotation = constr.get_rotate_by( neg_facing )
        if rel_rotation[0] != 0:
            self.rotating = True
        if self.rotation[1] > 0:
            self.ramping_up = True
        if self.rotation[1] < 0:
            self.ramping_down = True

        if -abs(self.speed) <= sin(pi*self.rotation[0]/2) <= abs(self.speed) or \
                -abs(self.speed) <= cos(pi*self.rotation[0]/2) <= abs(self.speed):
            angle = round(self.rotation[0]) % 4
            self.rotation[0] = angle
            if self.rotation[0] > 2:
                self.rotation[0] -= 4

            self.facing = facing_by_angle[angle]


        self.rotation[0] += 2*rel_rotation[0] * self.speed/ pi
        self.rotation[1] += 2*rel_rotation[1] * self.speed/ pi

        rotation = constr.get_rotate_to( neg_facing )
        if rotation[0] != 'None':
            self.rotation[0] = rotation[0]
        if rotation[1] != 'None':
            self.rotation[1] = rotation[1]
            if rotation[1] == 0:
                self.height = round(self.height)


        if not self.rotating:
            angle = round(self.rotation[0]) % 4
            self.rotation[0] = angle
            self.facing = facing_by_angle[angle]
            if self.rotation[0] > 2:
                self.rotation[0] -= 4

            if -abs(self.speed) <= sin(pi*self.rotation[0]/2) <= abs(self.speed):
                x = round(x)
            if -abs(self.speed) <= cos(pi*self.rotation[0]/2) <= abs(self.speed):
                y = round(y)

        self.position[0] = x
        self.position[1] = y

        self.stopped = False





class Train(Cart):
    carts: list[ Cart ]
    def __init__( self, cart_pack, carts_list, ):
        self.stopped = False 
        self.stopping = False 
        self.carts = carts_list
        self.cart_pack = cart_pack

    def get_carts(self):
        return self.carts
    def add_cart(self, cart):
        self.carts.append(cart)
    def delete_cart(self, cart_num):
        if cart_num >= len(self.carts) or len(self.carts) == 1:
            return False
        self.carts.pop(cart_num)
        return True

    def get_pos_list(self):
        pos_list = list()
        for cart in self.carts:
            pos_list.append(cart.get_tile())
        return pos_list

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
                cart.set_stopped(True)
            if self.stopping:
                cart.set_stopping(self.stopping)
            if cart.update(map, dont_move=True):
                self.stopped = True
        if not self.stopped:
            for cart in self.carts:
                if cart.update(map):
                    self.stopped = True

        if self.stopped:
            for cart in self.carts:
                cart.set_stopped( True )

    def get_stopped(self):
        return self.stopped
    def set_stopped(self, value):
        self.stopped = value
    def set_stopping(self, value):
        if value == "Toggle":
            self.stopping = not self.stopping
            self.stopped = False
            for cart in self.carts:
                cart.set_stopping("Toggle")
            return
        self.stopping = value

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













