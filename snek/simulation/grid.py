import random
import pygame

class Grid:
    def __init__(self, x: int = 50, y: int = 50):
        self.x = x
        self.y = y
        self.xa = random.randint(0, self.x)
        self.ya = random.randint(0, self.y)
        self.apple_size = 10
        self.apple = pygame.Rect(self.apple_size * self.xa, self.apple_size * self.ya, self.apple_size, self.apple_size)

    def interact(self, x: int, y: int) -> tuple[int, int]:
        """Interact agent move desire with world."""
        raise NotImplementedError
    
    def generate_apple(self):
        self.xa = random.randint(0, self.x)
        self.ya = random.randint(0, self.y)
        self.apple = pygame.Rect(self.apple_size * self.xa, self.apple_size * self.ya, self.apple_size, self.apple_size)


class GridWall(Grid):
    def interact(self, x: int, y: int) -> tuple[int, int]:
        x = min(max(x, 0), self.x-1)
        y = min(max(y, 0), self.y-1)
        return x, y


class GridLoop(Grid):
    def interact(self, x: int, y: int) -> tuple[int, int]:
        return x % self.x, y % self.y
