import pygame

from snek.simulation.agent import Agent
from snek.simulation.grid import Grid
from snek.simulation.consts import Color
from snek.simulation.score import Score
from snek.simulation.reward import Reward


def check_quit() -> bool:
    if pygame.event.get(eventtype=pygame.QUIT):
        pygame.quit()
        return False
    return True


class Game:
    def __init__(self, agent: Agent, grid: Grid, speed=15, manual_end=False):
        self.agent = agent
        self.grid = grid
        self.window = (agent.size_x*grid.x, agent.size_y*grid.y)
        self.speed = speed
        self.background = Color.BLACK
        self.end_condition = False
        self.manual_end = manual_end
        self.time = 0
        self.score = Score()
        self.reward = Reward()

        pygame.init()
        self.game_window = pygame.display.set_mode(self.window)
        self.fps = pygame.time.Clock()
        pygame.display.init()
        pygame.display.set_caption('snek')

    def update(self, train=False):
        x, y = self.agent.next_move()
        x, y, on_apple = self.grid.interact(x, y)
        if on_apple:
            self.grid.generate_apple(self.agent.body)
            self.score.prize()
            self.reward.reward_engine(apple_score=self.score.apple_score)
        self.end_condition = self.agent.update(x, y, on_apple)
        self.reward.reward_engine(dead = self.end_condition)
        if train:
            print('train')

    def draw(self):
        pygame.event.pump()
        self.game_window.fill(Color.BLACK.value)
        pygame.draw.rect(self.game_window, Color.RED.value, self.grid.apple)
        for sprite in self.agent.sprites:
            pygame.draw.rect(self.game_window, Color.GREEN.value, sprite)
        self.score.display(self.game_window)
        pygame.display.update()
        self.fps.tick(self.speed)
        self.time += 1

    def init(self):
        self.agent.init()
        self.grid.init(self.agent.body)
        self.time = 0
        self.score = Score()

    def play(self, train=False):
        self.grid.init(self.agent.body)

        while not self.end_condition:
            self.agent.interact()
            self.update(train=train)
            self.draw()
            if not check_quit():
                break
        else:
            self.game_over()
        return self.reward, self.time

    def game_over(self):
        game_over_font = pygame.font.Font(None, 50)
        game_over_surface = game_over_font.render('Git Gud', True, Color.WHITE.value)
        game_over_rect = game_over_surface.get_rect(topleft = (0,35))
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        if self.manual_end:
            while not pygame.event.peek(pygame.KEYDOWN) and not pygame.event.peek(pygame.QUIT):
                pass
        pygame.quit()
