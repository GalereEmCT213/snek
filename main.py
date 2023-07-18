from snek.simulation import Agent, GridLoop, GridWall, Game, RandomAgent

if __name__ == '__main__':
    # Normal game definition
    agent = Agent()
    grid = GridWall(x=50, y=50)
    normal_game = Game(agent, grid, speed=15, manual_end=True)

    # Random game definition (speed up)
    agent = RandomAgent(epsilon=0.1)
    grid = GridLoop()
    random_game = Game(agent, grid, speed=150, manual_end=False)

    # Change these lines
    # random_game.play()
    normal_game.play()
