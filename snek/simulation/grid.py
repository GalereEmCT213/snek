class Grid:
    def __init__(self, x: int = 50, y: int = 50):
        self.x = x
        self.y = y

    def interact(self, x: int, y: int) -> tuple[int, int]:
        raise NotImplementedError


class GridWall(Grid):
    def interact(self, x: int, y: int) -> tuple[int, int]:
        x = min(max(x, 0), self.x-1)
        y = min(max(y, 0), self.y-1)
        return x, y


class GridLoop(Grid):
    def interact(self, x: int, y: int) -> tuple[int, int]:
        return x % self.x, y % self.y
