
class PathfindingException(Exception):
    def __init__(self, tile, message="Tiles seems to be occupied"):
        self.tile = tile
        self.message = message
        super().__init__(self.message)

class AIPeopleException(Exception):
    def __init__(self, action, message="Not enough people to do the action"):
        self.action = action
        self.message = message
        super().__init__(self.message)