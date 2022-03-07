import math
import os
import pickle

import pygame
from pygame.time import delay

from BabyPanda import BabyPanda
from End import End
from MovingPlatform import MovingPlatform
from Platform import Platform
from Player import Player
from Ground import Ground
from Spikes import Spikes
from Tunnel import Tunnel
from World import World

pygame.init()
vec = pygame.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (56, 124, 68)
RED = (255, 0, 0)
BLUE = (209, 241, 255)
GREY = (194, 197, 204)
BROWN = (176, 146, 123)

SPRITE_SIZE = 50
colorList = (RED, GREEN, BLUE, BLACK, WHITE)


def imageLoad(duck, right_turn, number):
    if right_turn:
        if MyPlayer.no_of_pandas == 0:
            MyPlayer.image = pygame.image.load(
                os.path.join('resources', f'MyPlayer_{duck}right_nopanda{number}.png'))
        else:
            MyPlayer.image = pygame.image.load(
                os.path.join('resources', f'MyPlayer_{duck}right_panda{number}.png'))
    else:
        if MyPlayer.no_of_pandas == 0:
            MyPlayer.image = pygame.image.load(
                os.path.join('resources', f'MyPlayer_{duck}left_nopanda{number}.png'))
        else:
            MyPlayer.image = pygame.image.load(
                os.path.join('resources', f'MyPlayer_{duck}left_panda{number}.png'))


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("PandaRescue")

isJump = False
isFall = False

vel = 10
turn = 7

# running = True

all_sprites_list = pygame.sprite.Group()
my_player_list = pygame.sprite.Group()

moving_platforms_original_x = []

MyPlayer = Player(SPRITE_SIZE, SPRITE_SIZE, False, 1)
MyPlayer.rect.x = 0
MyPlayer.rect.y = 350
MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_right_nopanda.png'))

all_sprites_list.add(MyPlayer)
my_player_list.add(MyPlayer)

all_nonmoving_platform_sprites = pygame.sprite.Group()
end_group = pygame.sprite.Group()
all_spikes_group = pygame.sprite.Group()
all_tunnels_group = pygame.sprite.Group()
all_moving_plat_group = pygame.sprite.Group()
all_platform_sprites = pygame.sprite.Group()
all_panda_sprites = pygame.sprite.Group()
all_ground_sprites = pygame.sprite.Group()
all_sprites_on_mov_plat = pygame.sprite.Group()
background = pygame.image.load(os.path.join('resources', 'background3.png'))

# Matrix for creation of world conditions for a specific level

# world_data = [[0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0],
#               [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 4, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0],
#               [0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 7, 0, 0, 0, 0],
#               [8, 8, 8, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#               [8, 8, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
#               [8, 8, 8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 8, 8],
#               [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 8],
#               [8, [5, 7], 5, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 8, 8],
#               [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]

# Write world condition for a specific level to a file
# filename = 'level10'
# outfile = open(filename, 'wb')
# pickle.dump(world_data, outfile)
# outfile.close()

# Read world condition for a specific level from a file
# pickle_in = open(f'level9', 'rb')
pickle_in = open(f'level{MyPlayer.level}', 'rb')
world_data = pickle.load(pickle_in)

world = World(world_data)
grounds = []
end = 0
MyPlayer.points = 0
# Reading the world elements and assigning them to groups
for plat in world.tile_list:
    if type(plat) == Platform:
        all_nonmoving_platform_sprites.add(plat)
    elif type(plat) == End:
        end = plat.rect.x
        end_group.add(plat)
        all_sprites_on_mov_plat.add(plat)
    elif type(plat) == Spikes:
        all_spikes_group.add(plat)
        all_sprites_on_mov_plat.add(plat)
    elif type(plat) == Tunnel:
        all_tunnels_group.add(plat)
    elif type(plat) == MovingPlatform:
        moving_platforms_original_x.append(plat.rect.x)
        all_moving_plat_group.add(plat)
    elif type(plat) == BabyPanda:
        all_panda_sprites.add(plat)
        all_sprites_on_mov_plat.add(plat)
    elif type(plat) == Ground:
        grounds.append(plat.rect)
        all_sprites_list.add(plat)
        all_ground_sprites.add(plat)
        all_nonmoving_platform_sprites.add(plat)
    all_sprites_list.add(plat)

all_platform_sprites.add(all_moving_plat_group)
all_platform_sprites.add(all_nonmoving_platform_sprites)

running = True
movingRight = True

clock = pygame.time.Clock()

right = True
turn = 0

# Game Loop
level = MyPlayer.level

# Game Loop
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False
            elif event.key == pygame.K_SPACE:
                for plat in all_platform_sprites:
                    if plat.rect.top == MyPlayer.rect.bottom:
                        isJump = True
            elif event.key == pygame.K_RIGHT:
                right = True
                # MyPlayer.moving = True
            elif event.key == pygame.K_LEFT:
                right = False
                # MyPlayer.moving = True
            elif event.key == pygame.K_DOWN:
                if not MyPlayer.duck:
                    x = MyPlayer.rect.x
                    y = MyPlayer.rect.y + SPRITE_SIZE / 2
                    no_pandas = MyPlayer.no_of_pandas
                    MyPlayer.__init__(SPRITE_SIZE, SPRITE_SIZE / 2, True, level)
                    MyPlayer.rect.x = x
                    MyPlayer.rect.y = y
                    MyPlayer.no_of_pandas = no_pandas

                    # duck_string = ""
                    number = ""
                    # if MyPlayer.duck:
                    duck_string = "duck_"

                    imageLoad(duck_string, right, number)

            elif event.key == pygame.K_UP:
                if MyPlayer.duck:
                    x = MyPlayer.rect.x
                    y = MyPlayer.rect.y - SPRITE_SIZE / 2
                    no_pandas = MyPlayer.no_of_pandas
                    MyPlayer.__init__(SPRITE_SIZE, SPRITE_SIZE, False, level)
                    MyPlayer.rect.x = x
                    MyPlayer.rect.y = y
                    MyPlayer.no_of_pandas = no_pandas

                    duck_string = ""
                    number = ""
                    # if MyPlayer.duck:
                    #     duck_string = "duck_"

                    imageLoad(duck_string, right, number)

    keys = pygame.key.get_pressed()
    pressed_r = False
    pressed_l = False

    # Moving the players left and right
    if keys[pygame.K_RIGHT]:
        if not isJump and not isFall:
            MyPlayer.moveRight(SPRITE_SIZE / 5)
            isFall = True
        else:
            pressed_r = True
        collision = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
        if collision:
            MyPlayer.rect.right = collision[0].rect.left
        MyPlayer.moving = True
    elif keys[pygame.K_LEFT]:
        if not isJump and not isFall:
            MyPlayer.moveLeft(SPRITE_SIZE / 5)
            isFall = True
        else:
            pressed_l = True
        collision_side = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
        if collision_side:
            MyPlayer.rect.left = collision_side[0].rect.right
        MyPlayer.moving = True
    else:
        MyPlayer.moving = False

    # Moving of moving platforms and players on them
    count = 0
    for plat in all_moving_plat_group:
        if movingRight:
            if plat.rect.x <= moving_platforms_original_x[count] + 250:
                plat.rect.x += SPRITE_SIZE / 25

                if MyPlayer.rect.bottom == plat.rect.top:
                    if plat.rect.left < MyPlayer.rect.right < plat.rect.right:
                        MyPlayer.rect.x += SPRITE_SIZE / 25
                plat_col = pygame.sprite.spritecollide(MyPlayer, all_nonmoving_platform_sprites, False)
                if plat_col:
                    MyPlayer.rect.right = plat_col[0].rect.left

                for mov in all_moving_plat_group:
                    if MyPlayer.rect.left - 1 <= mov.rect.right <= MyPlayer.rect.left + 1 \
                            and MyPlayer.rect.y == mov.rect.y:
                        MyPlayer.moveRight(SPRITE_SIZE / 25)

                for pan in all_sprites_on_mov_plat:

                    if type(pan) == Spikes:
                        bottom = pan.rect.bottom - SPRITE_SIZE / 2
                    else:
                        bottom = pan.rect.bottom

                    if bottom == plat.rect.top:
                        if plat.rect.left < pan.rect.right < plat.rect.right:
                            pan.rect.x += SPRITE_SIZE / 25

                all_plat = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
                if not all_plat:
                    if not isJump and not isFall:
                        isFall = True
            else:
                movingRight = False
        elif not movingRight:
            if plat.rect.x >= moving_platforms_original_x[count] - 250:
                plat.rect.x -= SPRITE_SIZE / 25

                if MyPlayer.rect.bottom == plat.rect.top:
                    if plat.rect.left < MyPlayer.rect.right < plat.rect.right:
                        MyPlayer.rect.x -= SPRITE_SIZE / 25
                plat_col = pygame.sprite.spritecollide(MyPlayer, all_nonmoving_platform_sprites, False)
                if plat_col:
                    MyPlayer.rect.left = plat_col[0].rect.right

                for mov in all_moving_plat_group:
                    if MyPlayer.rect.right - 1 <= mov.rect.left <= MyPlayer.rect.right + 1 \
                            and MyPlayer.rect.y == mov.rect.y:
                        MyPlayer.moveLeft(SPRITE_SIZE / 25)

                for pan in all_sprites_on_mov_plat:

                    if type(pan) == Spikes:
                        bottom = pan.rect.bottom - SPRITE_SIZE / 2
                    else:
                        bottom = pan.rect.bottom

                    if bottom == plat.rect.top:
                        if plat.rect.left < pan.rect.right < plat.rect.right:
                            pan.rect.x -= SPRITE_SIZE / 25

                all_plat = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
                if not all_plat:
                    if not isJump and not isFall:
                        isFall = True
            else:
                movingRight = True
        count += 1

    # Actions connected to player's jumping
    if isJump:
        if vel > 0:
            MyPlayer.rect.y -= (2 * (vel ** 2)) / 5

            MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_jump.png'))

            if pressed_r:
                MyPlayer.rect.x += math.sqrt(abs(MyPlayer.rect.y))
                if MyPlayer.no_of_pandas == 0:
                    MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_jump_right_nopanda.png'))
                else:
                    MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_jump_right.png'))

            elif pressed_l:
                MyPlayer.rect.x -= math.sqrt(abs(MyPlayer.rect.y))
                if MyPlayer.no_of_pandas == 0:
                    MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_jump_left_nopanda.png'))
                else:
                    MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_jump_left.png'))

            vel -= 1
        elif vel == 0:
            MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall.png'))
            isJump = False
            isFall = True

        collision = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
        if collision:
            MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall.png'))
            MyPlayer.rect.top = collision[0].rect.bottom
            MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall.png'))
            isFall = True
            isJump = False
            vel = 0

    # Actions connected to player's falling
    if isFall:
        MyPlayer.rect.y += (2 * (vel ** 2)) / 5
        vel += 1

        if pressed_r:
            MyPlayer.rect.x += math.sqrt(abs(MyPlayer.rect.y))
            if MyPlayer.no_of_pandas == 0:
                MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall_right_nopanda.png'))
            else:
                MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall_right.png'))

        elif pressed_l:
            MyPlayer.rect.x -= math.sqrt(abs(MyPlayer.rect.y))
            if MyPlayer.no_of_pandas == 0:
                MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall_left_nopanda.png'))
            else:
                MyPlayer.image = pygame.image.load(os.path.join('resources', 'MyPlayer_fall_left.png'))

        collision = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
        if collision:
            MyPlayer.rect.bottom = collision[0].rect.top

            isFall = False
            isJump = False
            pressed_l = False
            pressed_r = False

            vel = 10

        collision_tun = pygame.sprite.spritecollide(MyPlayer, all_tunnels_group, False)
        if collision_tun:
            MyPlayer.rect.bottom = collision_tun[0].rect.bottom

            collision_ground = pygame.sprite.spritecollide(MyPlayer, all_platform_sprites, False)
            if collision_ground:
                MyPlayer.rect.bottom = collision_ground[0].rect.top
                isFall = False
                isJump = False

    # Displaying correct position of the player
    if not isJump and not isFall:
        duck_string = ""
        number = ""
        if MyPlayer.moving:
            number = "2"
        if MyPlayer.duck:
            duck_string = "duck_"
            number = ""

        imageLoad(duck_string, right, number)

    # Exiting and completing the current level
    completion = pygame.sprite.spritecollide(MyPlayer, end_group, False)
    if completion:
        # later - info about this level and transmission to next level
        level  = level + 1
        MyPlayer.level = level
        running = False

    # Collision with spikes
    spike_death = pygame.sprite.spritecollide(MyPlayer, all_spikes_group, False)
    if spike_death:
        MyPlayer.kill()
        running = False

    # Collecting baby pandas
    collect_panda = pygame.sprite.spritecollide(MyPlayer, all_panda_sprites, False)
    if collect_panda:
        MyPlayer.points += 10
        MyPlayer.no_of_pandas += 1
        x = collect_panda[0].rect.x
        y = collect_panda[0].rect.y
        collect_panda[0].kill()

    # Collision of moving platforms with non-moving ones
    for plat in all_moving_plat_group:
        moving_nonmoving = pygame.sprite.spritecollide(plat, all_nonmoving_platform_sprites, False)
        if moving_nonmoving:
            if movingRight:
                plat.rect.right = moving_nonmoving[0].rect.left
                movingRight = False
            else:
                plat.rect.left = moving_nonmoving[0].rect.right
                movingRight = True

    # Scrolling screen up and down
    if MyPlayer.rect.top <= SCREEN_HEIGHT / 5:
        for plat in all_sprites_list:
            plat.rect.y += SPRITE_SIZE / 5
    elif MyPlayer.rect.bottom > 4 * SCREEN_HEIGHT / 5:
        for plat in all_sprites_list:
            plat.rect.y -= SPRITE_SIZE / 5

    # Scrolling screen left and right
    if MyPlayer.rect.left >= 5 * SCREEN_WIDTH / 7:
        for plat in all_sprites_list:
            plat.rect.x -= SPRITE_SIZE / 5

        count = 0
        for plat in all_moving_plat_group:
            moving_platforms_original_x[count] -= SPRITE_SIZE / 5
            count += 1

    elif MyPlayer.rect.right <= 2 * SCREEN_WIDTH / 7:
        for plat in all_sprites_list:
            plat.rect.x += SPRITE_SIZE / 5
        count = 0
        for plat in all_moving_plat_group:
            moving_platforms_original_x[count] += SPRITE_SIZE / 5
            count += 1

    if MyPlayer.rect.top > 1000:
        delay(50)
        running = False

    # Updating and drawing
    all_nonmoving_platform_sprites.update()
    all_sprites_list.update()
    end_group.update()
    all_spikes_group.update()
    all_moving_plat_group.update()
    all_platform_sprites.update()
    all_tunnels_group.update()
    all_panda_sprites.update()
    my_player_list.update()

    all_nonmoving_platform_sprites.draw(screen)
    all_sprites_list.draw(screen)
    all_moving_plat_group.draw(screen)
    all_platform_sprites.draw(screen)
    all_tunnels_group.draw(screen)
    all_panda_sprites.draw(screen)
    my_player_list.draw(screen)
    end_group.draw(screen)
    all_spikes_group.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
