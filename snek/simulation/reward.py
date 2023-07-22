import numpy as np
from collections import deque

# Class for computing rewards and implementing reward engineering
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
        compare_dist = self._compare_distance(apple_pos, head)
        if not compare_dist:
            self.dist_factor = -1
        else:
            self.dist_factor = 1

        reward = self.apple_factor*appl + self.death_factor*dead + self.dist_factor
        reward += self.tick_factor*tick
        self.reward = reward
        self.history += reward

    def _dist_apple_head(
            self,
            apple: tuple, 
            head: tuple) -> float:
        """
        Calculates the manhattan distance between
        the snake's head and the apple

        :param apple: apple position on the grid
        :type apple: tuple of int
        :param head: snake's head position on the grid
        :type head: tuple of int
        :return: distance
        :type return: float
        """
        xa, ya = apple
        xh, yh = head

        return np.abs(xa-xh) + np.abs(ya-yh)
    
    def _compare_distance(
            self,
            apple: tuple,
            new_pos: tuple):
        """
        Compare if the snake's head gets closer or gets away
        from the apple
        """
        old_dist = self._dist_apple_head(apple, self.old_pos)
        new_dist = self._dist_apple_head(apple, new_pos)
        return old_dist > new_dist # True if closer
    
    def init(self):
        """
        Re-start the reward configuration
        """
        self.reward = 0
        self.history = 0
