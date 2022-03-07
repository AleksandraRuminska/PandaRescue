import os

import pygame

WHITE = (255, 255, 255)
GREY = (194, 197, 204)
DARK_GREY = (170, 170, 170)
SPRITE_SIZE = 50

image_up = pygame.image.load(os.path.join('resources', 'spikesu.png'))
image_down = pygame.image.load(os.path.join('resources', 'spikes_down.png'))


class Spikes(pygame.sprite.Sprite):

    def __init__(self, x, y, up):
        super().__init__()

        height = SPRITE_SIZE/2
        width = SPRITE_SIZE

        self.width = width
        self.height = height

        if up:
            self.image = image_up
            self.rect = self.image.get_rect()
            self.rect.y = y

        else:

            self.image = image_down
            self.rect = self.image.get_rect()
            self.rect.y = y + SPRITE_SIZE/2

        self.rect.x = x
