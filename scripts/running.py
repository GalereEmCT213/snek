import os
import numpy as np
import matplotlib.pyplot as plt

from snek.learning import DQNAgent
from snek.simulation import GridLoop, Game, GridWall

agent_name = 'burrice-artificial copy'
fig_format = 'png'
num_episodes = 1000
epsilon = 0.1
gamma = 0.95
batch_size = 128

agent = DQNAgent(epsilon=0, epsilon_min=0, state_size=(8,), action_size=4, gamma=gamma)
grid = GridWall(x=20, y=20)
game = Game(agent, grid, speed=150, manual_end=False)

agent.load(f'{agent_name}.h5')


while True:
    game.init()
    score, time = game.play(train=False)
    print(f'time: {time}, score: {score}')
