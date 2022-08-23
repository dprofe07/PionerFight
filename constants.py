# ***constants.py***
import pygame
import pygame.image
import pygame.font
import os

pygame.font.init()


class Color(tuple):
    def __eq__(self, other):
        return (super().__eq__(other) or
                (super().__eq__((255, 0, 0)) and other == 'red') or
                (super().__eq__((0, 255, 0)) and other == 'green') or
                (super().__eq__((255, 255, 255)) and other == 'white') or
                (super().__eq__((0, 0, 0)) and other == 'black')
                )


RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

WIDTH = 1200
HEIGHT = 400
BG = pygame.image.load('images/bg.jpg')

font = pygame.font.Font(None, 20)
health_font = pygame.font.Font(None, 20)
PAUSE_FONT = pygame.font.Font(None, 50)

START_POINTS = 1000
PAUSE_ADD_POINTS = 1
ADD_POINTS = 100
MAX_POINTS = 3000

WAIT_BEFORE_START = 5

LST_GREEN_KEYS = [
    pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
    pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0,
]

LST_RED_KEYS = [
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0
]
