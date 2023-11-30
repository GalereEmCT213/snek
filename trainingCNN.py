import os
import matplotlib.pyplot as plt

from snek.learning.cnn_agent import CNNAgent, CNNGame
from snek.simulation import Game, GridWall

from snek.simulation.consts import (
    AGENT_SIZE_X, 
    AGENT_SIZE_Y, 
    GRID_SIZE_X, 
    GRID_SIZE_Y)

agent_name = 'smart-snake'
fig_format = 'png'
num_episodes = 2000
epsilon = 1
gamma = 0.95
batch_size = 128

#############################
##     Set up training     ##
#############################
train = True

# Declares the enviroment and its objects
agent = CNNAgent(epsilon=epsilon, action_size=4, gamma=gamma, learning_rate=0.1)
grid = GridWall(x=GRID_SIZE_X, y=GRID_SIZE_Y)
game = CNNGame(agent, grid, speed=150, manual_end=False)

# Calls the NN file, if it exists
if os.path.exists(f'{agent_name}.h5'):
    agent.load(f'{agent_name}.h5')

done = False
batch_size = 32  # batch size used for the experience replay
reward_history = []
score_history = []

# Training execution
for episodes in range(1, num_episodes+1):
    game.init()
    
    reward, time = game.play(train=train)
    
    print(f'episode: {episodes}, time: {time}, reward: {reward}')
    reward_history.append(reward)
    score_history.append(game.get_game_score())

    game.agent.update_epsilon()

    # Plots results
    if episodes % 20 == 0:
        plt.subplot(211)
        plt.plot(reward_history, 'b')
        plt.title('Train Snake Game w/ Deep Q-Learning')
        plt.ylabel('Reward')
        plt.subplot(212)
        plt.plot(score_history, 'r')
        plt.ylabel('Game Score')
        plt.xlabel('Episode')
        plt.show(block=False)
        plt.pause(0.1)
        plt.savefig(f'dqn_training.{fig_format}', format=fig_format)
        agent.save(f'{agent_name}.h5')
