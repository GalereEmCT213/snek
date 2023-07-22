import pygame

from snek.simulation.consts import Color

class Score:
    def __init__(self, apple_score: int = 10):
        """
        Measures the number of points get 
        for eating apples.

        :param spple_score: points by each apple
        """
        self.apple_score = apple_score
        self.score = 0

    def prize(self):
        """
        Increase the game score after eating an apple
        """
        self.score += self.apple_score

    def display(self, game_window):
        """
        Print the score on the screen
        """
        score_font = pygame.font.Font(None, 30)
        score_surface = score_font.render(f'SCORE: {self.score:.0f}', True, Color.YELLOW.value)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)
    
    def init(self):
        """
        Re-start the game score
        """
        self.score = 0

    def get_score(self):
        """
        Get score when it is called
        """
        return self.score
