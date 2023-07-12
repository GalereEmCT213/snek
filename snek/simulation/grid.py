import random
import pygame
from collections import deque
from snek.simulation import agent

class Grid:
    def __init__(self, agent: agent.Agent, x: int = 50, y: int = 50):
        self.x = x
        self.y = y
        self.apple_size = 10
        self.generate_apple(agent.body)
        # self.xa = random.randint(0, self.x)
        # self.ya = random.randint(0, self.y)
        # self.apple = pygame.Rect(self.apple_size * self.xa, self.apple_size * self.ya, self.apple_size, self.apple_size)

    def interact(self, x: int, y: int) -> tuple[int, int, bool]:
        """Interact agent move desire with world."""
        raise NotImplementedError
    
    def generate_apple(self, body: deque):
        available_positions = [(x, y) for x in range(self.x) for y in range(self.y) if (x, y) not in body]

        if available_positions:
            self.xa, self.ya = random.choice(available_positions)
            self.apple = pygame.Rect(self.apple_size * self.xa, self.apple_size * self.ya, self.apple_size, self.apple_size)
        
        # TODO: implement else, which corresponds to game over win

    def check_apple(self, x: int, y: int) -> bool:
        return x == self.xa and y == self.ya


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
