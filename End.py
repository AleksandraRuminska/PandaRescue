import os
import random

import pygame

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SPRITE_SIZE = 50

image = pygame.image.load(os.path.join('resources', 'door.png'))


class End(pygame.sprite.Sprite):

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
