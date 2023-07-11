from snek.simulation import *

grid = GridLoop()
# grid = GridWall()
# agent = Agent()
agent = RandomAgent(epsilon=0.2)

game = Game(agent, grid, speed=10)
game.play()
