import os

import pygame

WHITE = (255, 255, 255)
GREY = (194, 197, 204)
DARK_GREY = (170, 170, 170)
SPRITE_SIZE = 50

image = pygame.image.load(os.path.join('resources', 'tunnel.png'))


class Tunnel(pygame.sprite.Sprite):

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
