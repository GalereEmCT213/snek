from snek.simulation import *

grid = GridLoop()
# grid = GridWall()
agent = Agent()

game = Game(agent, grid, speed=15)
game.play()
