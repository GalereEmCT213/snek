import numpy as np
from collections import deque

class Reward:
    
    def __init__(self) -> None:
        """
        Reward engineering based to be used in 
        Deep Q-Learning model
        """
        self.reward = 0
        self.death_factor = 1000

    def reward_engine(
            self, 
            apple_score: int = 0, 
            snake_body: deque = None,
            score_time: int = 0,
            dead: bool = False): 
        """
        Calculate the total reward after an update

        :param apple_score: score from catched apple 
        :param snake_len: length of the snake
        :param score_time: the time that has passed
        :param dead: indicates if the snake is still alive 
        """
        reward = apple_score - self.death_factor*dead
        self.reward += reward

    def get_reward(self):
        return self.reward

    def dist_apple_head(
            self,
            apple: tuple, 
            head: tuple) -> float:
        
        apple = np.array(apple)
        head = np.array(head)

        return np.ceil(np.linalg.norm(apple-head)).astype('int')