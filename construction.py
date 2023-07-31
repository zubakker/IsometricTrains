from json import loads

from math import pi


def load_construction_pack( name ):
    inp = open("construction_packs/" + name + ".json", "r").read()
    construction_pack = loads(inp)
    return construction_pack


class Construction:
    name: str
    facing: str # N, E, W, S, NE, ...

    def __init__( self, name, facing, type="construction" ):
        self.name = name
        self.facing = facing
        self.type = type
    def get_name_facing( self ):
        return self.name + "_" + self.facing
    def get_name( self ):
        return self.name
    def get_facing(self):
        return self.facing
    def get_type(self):
        return self.type
    ...

class Rail(Construction):
    come_from: list[str]
    rotate_to: dict[ str: str ]
    texture_scale: [float, float]
    texture_displacement: [float, float]

    def __init__( self, name, facing, constr_pack, c_type="rail" ):
        self.directions = "NESW"
        self.directions_rev = {
                "N": 0,
                "E": 1,
                "S": 2,
                "W": 3
                }
        self.rel_directions = ["Front", "Right", "Back", "Left"]
        self.rel_directions_rev = {
                "Front": 0,
                "Right": 1,
                "Back": 2,
                "Left": 3
                }
        super().__init__( name, facing, type=c_type )
        if not name:
            self.constr_pack = constr_pack
            return 
        self.come_from = constr_pack[self.type + " types"][ name ]["come_from"]
        self.rotate_by = constr_pack[self.type + " types"][ name ]["rotate_by"]
        self.rotate_to = constr_pack[self.type + " types"][ name ]["rotate_to"]
        self.required_tiles = constr_pack[self.type + " types"][ name ]["required_tiles"]
        self.texture_scale = constr_pack[self.type + " types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack[self.type + " types"][ name ]["texture_displacement"]
        self.texture_scale = constr_pack[self.type + " types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack[self.type + " types"][ name ]["texture_displacement"]
        self.layer_displacement = constr_pack[self.type + " types"][ name ]["layer_displacement"]
    def get_come_from( self ):
        come_fr = list()
        for dir in self.come_from:
            key = (self.directions_rev[self.facing] + self.rel_directions_rev[dir])%4
            come_fr.append(self.directions[key])
        return come_fr
    def get_rotate_to( self, come_from ):
        key_from = (self.directions_rev[come_from] - self.directions_rev[self.facing]) % 4
        rel_dir_from = self.rel_directions[key_from]
        if rel_dir_from in list(self.rotate_to):
            angle_hor, angle_ver = self.rotate_to[rel_dir_from]
            return [angle_hor, angle_ver]
        else:
            return ['None', 'None']

    def get_rotate_by( self, come_from ):
        key_from = (self.directions_rev[come_from] - self.directions_rev[self.facing]) % 4
        rel_dir_from = self.rel_directions[key_from]
        if rel_dir_from in list(self.rotate_by):
            angle_hor, angle_ver = self.rotate_by[rel_dir_from]
            return [angle_hor, angle_ver]
        else:
            return [0, 0]
    def get_required_tiles( self ):
        return self.required_tiles
    def get_texture_scale( self ):
        return self.texture_scale
    def get_texture_displacement( self ):
        return self.texture_displacement
    def get_layer_displacement( self ):
        return self.layer_displacement
    

    def output_json( self ):
        output = {
                "constr_type": self.type,
                "constr_name": self.name,
                "constr_facing": self.facing
                }
        return output
    def input_dict( self, input ):
        self.name = input["constr_name"]
        self.facing = input["constr_facing"]
        self.come_from = self.constr_pack[self.type + " types"][ self.name ]["come_from"]
        self.rotate_by = self.constr_pack[self.type + " types"][ self.name ]["rotate_by"]
        self.rotate_to = self.constr_pack[self.type + " types"][ self.name ]["rotate_to"]
        self.required_tiles = self.constr_pack[self.type + " types"][ self.name ]["required_tiles"]
        self.texture_scale = self.constr_pack[self.type + " types"][ self.name ]["texture_scale"]
        self.texture_displacement = self.constr_pack[self.type + " types"][ self.name ]["texture_displacement"]
        self.layer_displacement = self.constr_pack[self.type + " types"][ self.name ]["layer_displacement"]
    def input_json( self, json_txt ):
        input = loads(json_txt)
        self.input_dict(input)


class Station(Rail):
    def __init__(self, name, facing, constr_pack, map, pos):
        super().__init__(name, facing, constr_pack, c_type="station")
        if not name:
            self.constr_pack = constr_pack
            return 
        self.update_counter = 0
        self.inventory_space = constr_pack[self.type + " types"][ name ]["inventory_space"]
        self.updated_per_item = constr_pack[self.type + " types"][ name ]["updated_per_item"]
        self.inventory = list()
        self.not_loading = list()
        self.not_unloading = list()
        self.accepted_items = 'ANY' # TEMP
        # check for adjustment factories
        self.factories = list()
        x, y = pos.split(",")
        x, y = int(x), int(y)
        for i in range(-2, 3):
            for j in range(-2, 3):
                constr = map[str(x+i) +','+ str(y+j)][1]
                if not constr:
                    continue
                if constr.get_type() == "factory":
                    self.factories.append(constr)
                    constr.add_station(self)

    def get_status(self):
        if self.inventory:
            self.status = "stopping"
        else:
            self.status = "come through"
        return self.status
    def set_status(self, status):
        self.status = status

    def get_name_facing(self):
        if len(self.inventory) > 7: # TEMP
            return self.name + "_" + self.facing + "_7" # TEMP
        if not self.inventory:
            return self.name + "_" + self.facing 
        return self.name + "_" + self.facing + "_" + str(len(self.inventory))

    def get_items(self):
        return self.inventory[::]
    def remove_item(self, item):
        for i in range(len(self.inventory)):
            if self.inventory[i] == item:
                self.inventory.pop(i)
                return True
        return False
    def add_item(self, item):
        if (self.accepted_items == 'ANY' or item in self.accepted_items) and \
                len(self.inventory) < self.inventory_space:
            self.inventory.append(item)
            if item not in self.not_loading:
                self.not_loading.append(item)
            return True
        else:
            return False
    def load_item(self, item):
        if item in self.not_loading or len(self.inventory) == self.inventory_space:
            return False
        self.update_counter += 1
        if self.update_counter >= self.updated_per_item:
            self.update_counter = 0
            self.inventory.append(item)
            if item not in self.not_unloading:
                self.not_unloading.append(item)
            return "take item"
        return True
    def unload_item(self):
        for i, item in enumerate(self.inventory):
            if item not in self.not_unloading:
                self.update_counter += 1
                if self.update_counter >= self.updated_per_item:
                    self.update_counter = 0
                    self.inventory.pop(i)
                    return item
                return True
        return False
        
    def accepts_item(self, item):
        if not item:
            return False
        if self.accepted_items == 'ANY':
            return True
        elif item in self.accepted_items:
            return True
        return False
    def input_dict(self, input):
        super().input_dict(input)
        self.inventory_space = self.constr_pack[self.type + " types"][ self.name ]["inventory_space"]
        self.updated_per_item = self.constr_pack[self.type + " types"][ self.name ]["updated_per_item"]
        self.update_counter = 0
        self.inventory = input["constr_inventory"]
        self.not_loading = input["constr_not_loading"]
        self.not_unloading = input["constr_not_unloading"]
    def output_json(self):
        output = super().output_json()
        output["constr_inventory"] = self.inventory
        output["constr_not_loading"] = self.not_loading
        output["constr_not_unloading"] = self.not_unloading
        return output


class Factory(Construction):
    def __init__(self, name, facing, constr_pack):
        super().__init__(name, facing, constr_pack)
        self.type = "factory"
        if not name:
            self.constr_pack = constr_pack
            return 
        self.produced_item = constr_pack[self.type + " types"][ name ]["produced_item"]
        self.consumed_items = constr_pack[self.type + " types"][ name ]["consumed_items"]
        self.updated_per_item = constr_pack[self.type + " types"][ name ]["updated_per_item"]
        self.required_tiles = constr_pack[self.type + " types"][ self.name ]["required_tiles"]
        self.texture_scale = constr_pack[self.type + " types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack[self.type + " types"][ name ]["texture_displacement"]
        self.texture_scale = constr_pack[self.type + " types"][ name ]["texture_scale"]
        self.texture_displacement = constr_pack[self.type + " types"][ name ]["texture_displacement"]
        self.layer_displacement = constr_pack[self.type + " types"][ name ]["layer_displacement"]
        self.update_counter = 0
        self.stations = list()

    def add_station(self, station):
        self.stations.append(station)
    def get_required_tiles( self ):
        return self.required_tiles
    def get_texture_scale( self ):
        return self.texture_scale
    def get_texture_displacement( self ):
        return self.texture_displacement
    def get_layer_displacement( self ):
        return self.layer_displacement

    def update(self):
        self.update_counter += 1
        satisfied = True
        if not self.update_counter == self.updated_per_item:
            return
        self.update_counter = 0
        for item in self.consumed_items:
            item_satisfied = False
            for station in self.stations:
                if item in station.get_items():
                    item_satisfied = True
            if not item_satisfied:
                satisfied = False
                break
        if satisfied:
            for item in self.consumed_items:
                for station in self.stations:
                    if item in station.get_items():
                        station.remove_item(item)
                        break
            for station in self.stations:
                if station.accepts_item(self.produced_item) and station.add_item(self.produced_item):
                    break
    def output_json( self ):
        output = {
                "constr_type": self.type,
                "constr_name": self.name,
                "constr_facing": self.facing,
                "constr_upd_counter": self.update_counter
                }
        return output
    def input_dict( self, input ):
        self.type = input["constr_type"]
        self.name = input["constr_name"]
        self.facing = input["constr_facing"]
        self.update_counter = input["constr_upd_counter"]
        self.produced_item = self.constr_pack[self.type + " types"][ self.name ]["produced_item"]
        self.consumed_items = self.constr_pack[self.type + " types"][ self.name ]["consumed_items"]
        self.updated_per_item = self.constr_pack[self.type + " types"][ self.name ]["updated_per_item"]
        self.required_tiles = self.constr_pack[self.type + " types"][ self.name ]["required_tiles"]
        self.texture_scale = self.constr_pack[self.type + " types"][ self.name ]["texture_scale"]
        self.texture_displacement = self.constr_pack[self.type + " types"][ self.name ]["texture_displacement"]
        self.layer_displacement = self.constr_pack[self.type + " types"][ self.name ]["layer_displacement"]
        self.stations = list()
    def input_json( self, json_txt ):
        input = loads(json_txt)
        self.input_dict(input)




