from item import Item


class Cart:
    name: str 
    inventory: list[ Item ]
    ...

class Train:
    carts: list[ Cart ]
    ...
