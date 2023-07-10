from snek.simulation import *

grid = GridLoop()
# grid = GridWall()
# agent = Agent()
agent = RandomAgent(epsilon=0.1)

game = Game(agent, grid, speed=100)
game.play()
