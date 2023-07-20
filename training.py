import os
import numpy as np
import matplotlib.pyplot as plt

from snek.learning import DQNAgent
from snek.simulation import GridLoop, Game, GridWall

agent_name = 'burrice-artificial'
fig_format = 'png'
num_episodes = 1000
epsilon = 0.25
gamma = 0.95
batch_size = 32  # 128
grid_size_x = 20
grid_size_y = 20

agent = DQNAgent(epsilon=epsilon, state_size=(grid_size_x,grid_size_y,3), action_size=4, gamma=gamma)
grid = GridWall(x=grid_size_x, y=grid_size_y)
game = Game(agent, grid, speed=150, manual_end=False)

# if os.path.exists(f'{agent_name}.h5'):
#     agent.load(f'{agent_name}.h5')


done = False
batch_size = 32  # batch size used for the experience replay
return_history = []

for episodes in range(1, num_episodes+1):
    game.init()
    
    score, time = game.play(train=True)
    print(f'episode: {episodes}, time: {time}, score: {score}')

    game.agent.update_epsilon()
    if episodes % 20 == 0:
    #     plt.plot(return_history, 'b')
    #     plt.xlabel('Episode')
    #     plt.ylabel('Return')
    #     plt.show(block=False)
    #     plt.pause(0.1)
    #     plt.savefig(f'dqn_training.{fig_format}', format=fig_format)
        agent.save(f'{agent_name}.h5')
