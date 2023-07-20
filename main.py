from snek.simulation import PlayerAgent, GridLoop, GridWall, Game, RandomAgent

if __name__ == '__main__':
    # Normal game definition
    agent = PlayerAgent()
    grid = GridWall(x=20, y=20)
    normal_game = Game(agent, grid, speed=1, manual_end=True)

    # Random game definition (speed up)
    agent = RandomAgent(epsilon=0.1)
    grid = GridLoop()
    random_game = Game(agent, grid, speed=150, manual_end=False)

    # Change these lines
    # random_game.play()
    normal_game.play()
