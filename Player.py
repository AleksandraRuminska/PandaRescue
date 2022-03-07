import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
vec = pygame.math.Vector2
SPRITE_SIZE = 50
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, duck, level):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(WHITE)

        self.no_of_pandas = 0
        self.duck = duck
        self.level = level
        self.level_completed = False
        self.points = 0
        self.moving = False
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels
