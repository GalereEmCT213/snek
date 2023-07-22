from enum import Enum

import pygame

# Enum with a list of possible movements (Left, Up, Down, Right) in cartesian coordinates
class Move(Enum):
    L = (-1, 0)
    U = (0, -1)
    D = (0, 1)
    R = (1, 0)


# Enum with a list of pygame colors used in the project
class Color(Enum):
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    YELLOW = pygame.Color(255, 255, 0)
