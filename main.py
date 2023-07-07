from snek.simulation import *

grid = GridLoop()
# grid = GridWall()
agent = Agent()

game = Game(agent, grid, speed=10)
game.play()
