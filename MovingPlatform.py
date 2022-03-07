import os

import pygame

WHITE = (255, 255, 255)
GREEN = (26, 160, 90)
SPRITE_SIZE = 50

image = pygame.image.load(os.path.join('resources', 'moving_plat.png'))


class MovingPlatform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        height = SPRITE_SIZE
        width = SPRITE_SIZE*2

        self.width = width
        self.height = height

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
