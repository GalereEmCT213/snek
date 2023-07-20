import random
import pygame
from collections import deque


class Grid:
    def __init__(self, x: int = 50, y: int = 50):
        self.x = x
        self.y = y
        self.apple_size = 10
        self.xa = random.randint(0, self.x)
        self.ya = random.randint(0, self.y)
        self.apple = pygame.Rect(self.apple_size * self.xa, self.apple_size * self.ya, self.apple_size, self.apple_size)
    
    def generate_apple(self, body: deque[tuple[int, int]]):
        drop_set = set(body)
        positions = {(x, y) for x in range(self.x) for y in range(self.y)}
        available_positions = positions - drop_set

        if available_positions:
            self.xa, self.ya = random.choice(list(available_positions))
            self.apple = pygame.Rect(self.apple_size*self.xa, self.apple_size*self.ya, self.apple_size, self.apple_size)
        
        return self.xa, self.ya

    def check_apple(self, x: int, y: int) -> bool:
        return x == self.xa and y == self.ya

    def init(self, agent_body: deque[tuple[int, int]]):
        return self.generate_apple(agent_body)
    
    def interact(self, x: int, y: int) -> tuple[int, int, bool]:
        """Interact agent move desire with world."""
        raise NotImplementedError


class GridWall(Grid):
    def interact(self, x: int, y: int) -> tuple[int, int, bool]:
        x = min(max(x, 0), self.x-1)
        y = min(max(y, 0), self.y-1)
        on_apple = self.check_apple(x, y)
        return x, y, on_apple


class GridLoop(Grid):
    def interact(self, x: int, y: int) -> tuple[int, int, bool]:
        x %= self.x
        y %= self.y
        on_apple = self.check_apple(x, y)
        return x, y, on_apple
