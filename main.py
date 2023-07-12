from snek.simulation import *

grid = GridLoop(x=10, y=10)
# grid = GridWall()
# agent = Agent()
agent = RandomAgent(epsilon=0.1)

game = Game(agent, grid, speed=15)
game.play()
