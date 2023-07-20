import numpy as np
from collections import deque

class Reward:
    
    def __init__(self) -> None:
        """
        Reward engineering based to be used in 
        Deep Q-Learning model
        """
        self.reward = 0
        self.history = 0
        self.death_factor = -100
        self.apple_factor = 10
        self.tick_factor = 1
        self.dist_factor = 1
        self.old_pos = (0,0)

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
        head = snake_body[0]
        self.dist = self._dist_apple_head(apple_pos, head)
        # print(f"dist: {self.dist} ====== apple: {apple_pos} ======= head: {head}")
        compare_dist = self._compare_distance(apple_pos, head)
        if not compare_dist:
            self.dist_factor = -1
        else:
            self.dist_factor = 1

        reward = self.apple_factor*appl + self.death_factor*dead + self.dist_factor
        self.reward = reward
        self.history += reward

    def _dist_apple_head(
            self,
            apple: tuple, 
            head: tuple) -> float:
        
        xa, ya = apple
        xh, yh = head

        return np.abs(xa-xh) + np.abs(ya-yh)
    
    def _compare_distance(
            self,
            apple: tuple,
            new_pos: tuple):
        old_dist = self._dist_apple_head(apple, self.old_pos)
        new_dist = self._dist_apple_head(apple, new_pos)
        return old_dist > new_dist # True if closer
    
    def init(self):
        self.reward = 0
        self.history = 0
