from collections import deque
import pygame
import random

from snek.simulation.consts import Move


class Agent:
    def __init__(self, x: int = 0, y: int = 0, direction: Move = Move.R, initial_size: int = 5):
        self.initial_size = initial_size
        self.x, self.y = x, y
        self.body = deque((x + i, y + 5) for i in reversed(range(initial_size)))
        self.size_x, self.size_y = (10, 10)
        self.sprites = deque(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y) for x, y in self.body)
        self.initial_direction = direction
        self.direction = direction
        self.next_direction = direction

    def interact(self):
        """Agent interaction with world.

        Here, the agent takes decision from which direction it's going to choose. For the gameplay, it just
        looks for input key press. However, for AI agent, this method should decide the best next move.
        TODO: implement the interact for the AI agent.
        """

        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            match event.key:
                case pygame.K_UP:
                    self.next_direction = Move.U
                case pygame.K_DOWN:
                    self.next_direction = Move.D
                case pygame.K_LEFT:
                    self.next_direction = Move.L
                case pygame.K_RIGHT:
                    self.next_direction = Move.R

    def update(self, x: int, y: int, on_apple: bool, reward=None) -> bool:
        """Update position.

        Updates the agent position based on the interaction with world. Updates both body position and sprites.
        """
        if not on_apple:
            self.body.pop()
            self.sprites.pop()
        
        print(reward)

        self.x, self.y = x, y
        self.body.appendleft((x, y))
        self.sprites.appendleft(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y))

        return self.body[0] in list(self.body)[1:]  # Memory usage?

    def validate_next_move(self) -> bool:
        match self.direction:
            case Move.R: return self.next_direction != Move.L
            case Move.L: return self.next_direction != Move.R
            case Move.U: return self.next_direction != Move.D
            case Move.D: return self.next_direction != Move.U
        return True

    def next_move(self) -> tuple[int, int]:
        """Agent next move based on direction and location."""
        if self.validate_next_move():
            self.direction = self.next_direction

        x, y = self.body[0]
        vx, vy = self.direction.value

        return x+vx, y+vy

    def init(self):
        self.direction = self.initial_direction
        self.next_direction = self.initial_direction
        self.body = deque((self.x + i, self.y + 5) for i in reversed(range(self.initial_size)))
        self.sprites = deque(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y) for x, y in self.body)


class RandomAgent(Agent):
    def __init__(self, *args, epsilon: float = 0.1, **kwargs):
        self.epsilon = epsilon
        super().__init__(*args, **kwargs)

    def interact(self):
        if random.random() < self.epsilon:
            self.next_direction = random.choice([Move.L, Move.R, Move.D, Move.U])

