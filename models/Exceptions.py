
class PathfindingException(Exception):
    def __init__(self, tile, message="Tiles seems to be occupied"):
        self.tile = tile
        self.message = message
        super().__init__(self.message)