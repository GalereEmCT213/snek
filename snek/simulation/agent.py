from collections import deque
import pygame
import random

from snek.simulation.consts import Move

from snek.simulation.consts import AGENT_SIZE_X, AGENT_SIZE_Y

# Base Snake-Playing Agent Class
class Agent:
    def __init__(
            self, 
            x: int = 0,
            y: int = 0, 
            direction: Move = Move.R, 
            initial_size: int = 3, 
            gamma: float = 0.9):
        self.initial_size = initial_size
        self.x, self.y = x, y
        self.body = deque((x + i, y + 5) for i in reversed(range(initial_size)))
        self.size_x, self.size_y = (AGENT_SIZE_X, AGENT_SIZE_Y)
        self.sprites = deque(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y) for x, y in self.body)
        self.initial_direction = direction
        self.direction = direction
        self.next_direction = direction
        self.gamma = gamma

    def update(
            self, 
            x: int, 
            y: int, 
            on_apple: bool) -> bool:
        """Update position.

        Updates the agent position based on the interaction with world. Updates both body position and sprites.

        :return: check if snake head has collided with body
        :type return: bool
        """
        if not on_apple:
            self.body.pop()
            self.sprites.pop()

        self.x, self.y = x, y
        self.body.appendleft((x, y))
        self.sprites.appendleft(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y))

        return self.body[0] in list(self.body)[1:] 

    def validate_next_move(self) -> bool:
        """Validate next move, by forbidding snake from moving backwards.
        
        :type return: bool
        """
        match self.direction:
            case Move.R: return self.next_direction != Move.L
            case Move.L: return self.next_direction != Move.R
            case Move.U: return self.next_direction != Move.D
            case Move.D: return self.next_direction != Move.U
        return True

    def next_move(self) -> tuple[int, int]:
        """Agent next move based on direction and location.
        
        :return: new position coordinates
        :type return: tuple of int
        """
        if self.validate_next_move():
            self.direction = self.next_direction

        x, y = self.body[0]
        vx, vy = self.direction.value

        return x+vx, y+vy

    def init(self, x, y):
        """Restarts snake for new game."""
        
        self.x, self.y = x, y
        self.direction = self.initial_direction
        self.next_direction = self.initial_direction
        self.body = deque((self.x + i, self.y + 5) for i in reversed(range(self.initial_size)))
        self.sprites = deque(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y) for x, y in self.body)

    def interact(self, state):
        """Agent interaction with world."""
        raise NotImplementedError

    def train(self, state, action, reward, next_state, done):
        """Method for training the agent"""
        raise NotImplementedError

    def update_epsilon(self):
        """Method for epsilon scheduling"""
        raise NotImplementedError


# Inherited Agent class, with random direction policy

class RandomAgent(Agent):
    def __init__(
            self, 
            *args, 
            epsilon: float = 0.1, 
            **kwargs):
        self.epsilon = epsilon
        super().__init__(*args, **kwargs)

    def interact(self, state):
        """Interact with game, changing direction at random."""
        if random.random() < self.epsilon:
            self.next_direction = random.choice([Move.L, Move.R, Move.D, Move.U])


# Inherited Agent class, with directions set by user
class PlayerAgent(Agent):
    def interact(self, state):
        """Interact with game, by getting user input."""
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
