from item import Item


class Cart:
    name: str 
    position: [float, float]
    speed: float
    facing: ...
    inventory: list[ Item ]
    
    ...

class Train:
    carts: list[ Cart ]
    ...
