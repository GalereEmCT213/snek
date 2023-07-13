import numpy as np
import matplotlib.pyplot as plt
from snek.simulation import RandomAgent, Game, GridWall


def run_simulation(epsilon: float = 0.1, speed: int = 1000):
    agent = RandomAgent(epsilon=epsilon)
    grid = GridWall()
    game = Game(agent, grid, speed=speed, manual_end=False)
    return game.play()


if __name__ == '__main__':
    epsilon_list = np.arange(1, step=0.1)
    average_list = []
    episodes = 100

    for epsilon in epsilon_list:
        time_history = []
        for _ in range(episodes):
            _, time = run_simulation(epsilon, speed=1000000)
            time_history.append(time)

        avg = np.average(time_history)
        average_list.append(avg)
        print(f'{epsilon=} {avg=}')

    plt.plot(epsilon_list, average_list)
    plt.show()

    # episodes = 100
    # for _ in range(episodes):
    #     _, time = run_simulation(speed=1000000)
    #     print(time)
