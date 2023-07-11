from collections import deque
import pygame
import random

from snek.simulation.consts import Move


class Agent:
    def __init__(self, x: int = 0, y: int = 0, direction: Move = Move.R):
        self.initial_size = 5
        self.body = deque([(x + i, y + 5) for i in range(self.initial_size)])
        self.size_x, self.size_y = (10, 10)
        self.sprites = deque([pygame.Rect(coord[0] * self.size_x, coord[1] * self.size_y, self.size_x, self.size_y) for coord in self.body])
        self.direction = direction
        self.next_direction = direction

    def interact(self):
        """Agent interaction with world.

        Here, the agent takes decision from which direction it's going to choose. For the gameplay, it just
        looks for input key press. However, for AI agent, this method should decide the best next move.
        TODO: implement the interact for the AI agent.
        """

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

    def update(self, x: int, y: int, on_apple: bool) -> bool:
        """Update position.

        Updates the agent position based on the interaction with world. Updates both body position and sprites.
        """
        if not on_apple:
            self.body.pop()
            self.sprites.pop()

        self.body.appendleft((x, y))
        self.sprites.appendleft(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y))

        return self.body[0] in self.body

    
    def validate_next_move(self, current_direction, next_direction) -> bool:
        if current_direction == Move.U and next_direction == Move.D:
            return False
        elif current_direction == Move.D and next_direction == Move.U:
            return False
        elif current_direction == Move.L and next_direction == Move.R:
            return False
        elif current_direction == Move.R and next_direction == Move.L:
            return False
        
        return True

    def next_move(self) -> tuple[int, int]:
        """Agent next move based on direction and location."""
        if self.validate_next_move(self.direction, self.next_direction):
            self.direction = self.next_direction

        x, y = self.body[0]
        vx, vy = self.direction.value

        return x+vx, y+vy


class RandomAgent(Agent):
    def __init__(self, epsilon: float = 0.1, *args, **kwargs):
        self.epsilon = epsilon
        super().__init__(*args, **kwargs)

    def interact(self):
        if random.random() < self.epsilon:
            self.next_direction = random.choice([Move.L, Move.R, Move.D, Move.U])

