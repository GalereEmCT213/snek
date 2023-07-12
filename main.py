from snek.simulation import *

# agent = Agent()
agent = RandomAgent(epsilon=0.1)
# grid = GridLoop(agent, x=50, y=50)
grid = GridWall(agent)

game = Game(agent, grid, speed=15)
game.play(manual_end=True)

