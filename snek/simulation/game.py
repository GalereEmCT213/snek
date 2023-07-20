import pygame
import numpy as np

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
    def __init__(self, agent: Agent, grid: Grid, reward: Reward = Reward(), speed=15, manual_end=False):
        self.agent = agent
        self.grid = grid
        self.reward = reward
        self.window = (agent.size_x*grid.x, agent.size_y*grid.y)
        self.speed = speed
        self.background = Color.BLACK
        self.end_condition = False
        self.manual_end = manual_end
        self.time = 0
        self.score = Score()
        self.cumulative_reward = 0

        pygame.init()
        self.game_window = pygame.display.set_mode(self.window)
        self.fps = pygame.time.Clock()
        pygame.display.init()
        pygame.display.set_caption('snek')

    def update(self):
        x, y = self.agent.next_move()
        x, y, on_apple = self.grid.interact(x, y)
        if on_apple:
            self.apple = self.grid.generate_apple(self.agent.body)
            self.score.prize()
        self.end_condition = self.agent.update(x, y, on_apple)
        self.reward.reward_engine(tick=True, dead=self.end_condition, appl=on_apple, snake_body=self.agent.body, apple_pos=self.apple)
        self.cumulative_reward = self.agent.gamma * self.cumulative_reward + self.reward.reward

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
        self.agent.init(x=0, y=0)
        self.grid.init(self.agent.body)
        self.reward.init()
        self.time = 0
        self.cumulative_reward = 0
        self.end_condition = False
        self.score = Score()
        self.apple = (self.grid.xa, self.grid.ya)


    def play(self, train=False):
        self.grid.init(self.agent.body)
        state = self._generate_state()

        while not self.end_condition:
            self.agent.interact(state)
            self.update()

            if train:
                action = self.agent.direction
                reward = self.reward.reward
                done = self.end_condition
                next_state = self._generate_state()
                next_state = next_state
                self.agent.train(state, action, reward, next_state, done)
                state = next_state

            self.draw()
            if not check_quit():
                break
        else:
            self.game_over()
        
        if train:
            self.agent.update_epsilon()

        return self.reward.reward, self.time

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

    def _generate_state(self):
        sx, sy = self.grid.x, self.grid.y  # Grid size
        state = np.zeros((sx, sy, 3))  # Initialize state

        state[self.grid.xa, self.grid.ya, 0] = 1  # Apple position
        state[self.agent.body[0][0], self.agent.body[0][1], 1] = 1  # Agent head position

        for x, y in self.agent.body:
            state[x, y, 2] = 1  # Agent body position
        
        return state[np.newaxis, :]

