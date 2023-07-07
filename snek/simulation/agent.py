from collections import deque
import pygame

from snek.simulation.consts import Move


class Agent:
    def __init__(self, x: int = 0, y: int = 0, direction: Move = Move.R):
        self.body = deque([(x, y)])
        self.size_x, self.size_y = (10, 10)
        self.sprites = deque([pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y)])
        self.direction = direction

    def interact(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.direction = Move.U
                    case pygame.K_DOWN:
                        self.direction = Move.D
                    case pygame.K_LEFT:
                        self.direction = Move.L
                    case pygame.K_RIGHT:
                        self.direction = Move.R

    def update(self, x: int, y: int) -> bool:
        self.body.pop()
        self.body.appendleft((x, y))
        self.sprites.pop()
        self.sprites.appendleft(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y))
        return self.body[0] in self.body

    def next_move(self) -> tuple[int, int]:
        x, y = self.body[0]
        vx, vy = self.direction.value
        return x+vx, y+vy
