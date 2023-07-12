from snek.simulation import *

# Normal game definition
agent = Agent()
grid = GridWall(agent, x=50, y=50)
normal_game = Game(agent, grid, speed=15, manual_end=True)

# Random game definition (speed up)
agent = RandomAgent(epsilon=0.1)
grid = GridWall(agent)
random_game = Game(agent, grid, speed=15, manual_end=False)


if __name__ == '__main__':
    # random_game.play()
    normal_game.play()
