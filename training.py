import os
import matplotlib.pyplot as plt

from snek.learning import DQNAgent
from snek.simulation import Game, GridWall

agent_name = 'burrice-artificial'
fig_format = 'png'
num_episodes = 1000
epsilon = 1
gamma = 0.95
batch_size = 256  # 128
grid_size_x = 20
grid_size_y = 20

#############################
##     Set up training     ##
#############################
train = True

# Declares the enviroment and its objects
agent = DQNAgent(epsilon=epsilon, state_size=(12,), action_size=4, gamma=gamma)
grid = GridWall(x=grid_size_x, y=grid_size_y)
game = Game(agent, grid, speed=150, manual_end=False)

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
