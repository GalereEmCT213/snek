import pygame

from snek.simulation.agent import Agent
from snek.simulation.grid import Grid
from snek.simulation.consts import Color


def check_quit() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
    return True


class Game:
    def __init__(self, agent: Agent, grid: Grid, speed=15):
        self.agent = agent
        self.grid = grid
        self.window = (agent.size_x*grid.x, agent.size_y*grid.y)
        self.speed = speed
        self.background = Color.BLACK
        self.end_condition = False

        pygame.init()
        self.game_window = pygame.display.set_mode(self.window)
        self.fps = pygame.time.Clock()
        pygame.display.init()
        pygame.display.set_caption('snek')

    def update(self):
        x, y = self.agent.next_move()
        x, y, on_apple = self.grid.interact(x, y)
        if on_apple:
            self.grid.generate_apple(self.agent.body)
        self.end_condition = self.agent.update(x, y, on_apple)

    def draw(self):
        pygame.event.pump()
        self.game_window.fill(Color.BLACK.value)
        pygame.draw.rect(self.game_window, Color.RED.value, self.grid.apple)
        for sprite in self.agent.sprites:
            pygame.draw.rect(self.game_window, Color.GREEN.value, sprite)
        pygame.display.update()
        self.fps.tick(self.speed)

    def play(self):
        while check_quit() and not self.end_condition:
            self.agent.interact()
            self.update()
            self.draw()

        if self.end_condition:
            self.game_over()

    def game_over(self):
        game_over_font = pygame.font.Font(None, 50)
        game_over_surface = game_over_font.render('Git Gud', True, Color.WHITE.value)
        game_over_rect = game_over_surface.get_rect()
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()