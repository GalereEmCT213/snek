import numpy as np
from collections import deque

class Reward:
    
    def __init__(self) -> None:
        """
        Reward engineering based to be used in 
        Deep Q-Learning model
        """
        self.reward = 0
        self.death_factor = -1000
        self.apple_factor = 100
        self.tick_factor = 1
        self.dist_factor = -10

    def reward_engine(
            self,
            snake_body: deque = None,
            apple_pos: tuple = None,
            appl: bool = False,
            dead: bool = False,
            tick: bool = False,
        ): 
        """
        Calculate the total reward after an update

        :param apple_score: score from catched apple 
        :param snake_len: length of the snake
        :param score_time: the time that has passed
        :param dead: indicates if the snake is still alive 
        """
        if apple_pos is not None and snake_body is not None:
            head = snake_body[0]
            self.dist = self._dist_apple_head(apple_pos, head)

        reward = self.apple_factor*appl + self.death_factor*dead + self.tick_factor*tick + self.dist_factor*self.dist
        self.reward += reward

    def _dist_apple_head(
            self,
            apple: tuple, 
            head: tuple) -> float:
        
        apple = np.array(apple)
        head = np.array(head)

        return np.ceil(np.linalg.norm(apple-head)).astype('int')
    
    def init(self):
        self.reward = 0
