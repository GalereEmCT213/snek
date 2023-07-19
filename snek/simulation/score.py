import pygame

from snek.simulation.consts import Color

class Score:
    def __init__(self, apple_score: int = 100, time_score: int = 1):
        self.apple_score = apple_score
        self.score = 0

    def prize(self):
        self.score += self.apple_score

    def get_score(self):
        return self.score

    def display(self, game_window):
        score_font = pygame.font.Font(None, 30)
        score_surface = score_font.render(f'SCORE: {self.score:.0f}', True, Color.YELLOW.value)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)