import pygame

from snek.simulation.agent import Agent
from snek.simulation.grid import Grid
from snek.simulation.consts import Color


class Game:
    def __init__(self, agent: Agent, grid: Grid, speed=15):
        self.agent = agent
        self.grid = grid
        self.window = (agent.size_x*grid.x, agent.size_y*grid.y)
        self.speed = speed
        self.background = Color.BLACK

        pygame.init()
        self.game_window = pygame.display.set_mode(self.window)
        self.fps = pygame.time.Clock()
        pygame.display.set_caption('snek')

    def update(self):
        x, y = self.agent.next_move()
        x, y = self.grid.interact(x, y)
        return self.agent.update(x, y)

    def draw(self):
        self.game_window.fill(Color.BLACK.value)
        for sprite in self.agent.sprites:
            pygame.draw.rect(self.game_window, Color.GREEN.value, sprite)
        pygame.display.update()
        self.fps.tick(self.speed)

    def play(self):
        while True:
            self.agent.interact()
            self.update()
            self.draw()
