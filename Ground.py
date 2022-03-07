import os
import random

import pygame

WHITE = (255, 255, 255)
GREEN = (26, 160, 90)
SPRITE_SIZE = 50
BROWN = (176, 146, 123)
BLACK = (0, 0, 0)

image = pygame.image.load(os.path.join('resources', 'ground.png'))


class Ground(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        height = SPRITE_SIZE
        width = SPRITE_SIZE

        self.width = width
        self.height = height

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
