from tile import Tile, Map


class Camera:
    position: [float, float]
    zoom: float
    
    def render( map: Map ):
        ...

