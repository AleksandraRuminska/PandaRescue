from BabyPanda import BabyPanda
from End import End
from Ground import Ground
from MovingPlatform import MovingPlatform
from Platform import Platform
from Spikes import Spikes
from Tunnel import Tunnel

WHITE = (255, 255, 255)
GREEN = (26, 160, 90)
SPRITE_SIZE = 50


class World:
    def __init__(self, w_data):
        self.tile_list = []

        row_count = 0
        for row in w_data:
            col = 0
            for tile in row:
                if type(tile) == int:
                    self.tileRecogn(tile, col, row_count)
                else:
                    for elem in tile:
                        self.tileRecogn(elem, col, row_count)
                col += 1
            row_count += 1

    def tileRecogn(self, tile, col, row_count):
        if tile == 1:
            platform = Platform(col * SPRITE_SIZE, row_count * SPRITE_SIZE)
            self.tile_list.append(platform)
        elif tile == 2:
            end = End(col * SPRITE_SIZE, row_count * SPRITE_SIZE)
            self.tile_list.append(end)
        elif tile == 3:
            spikes_down = Spikes(col * SPRITE_SIZE, row_count * SPRITE_SIZE, 0)
            self.tile_list.append(spikes_down)
        elif tile == 4:
            spikes = Spikes(col * SPRITE_SIZE, row_count * SPRITE_SIZE, 1)
            self.tile_list.append(spikes)
        elif tile == 5:
            tunnel = Tunnel(col * SPRITE_SIZE, row_count * SPRITE_SIZE)
            self.tile_list.append(tunnel)
        elif tile == 6:
            mov_plat = MovingPlatform(col * SPRITE_SIZE, row_count * SPRITE_SIZE)
            self.tile_list.append(mov_plat)
        elif tile == 7:
            panda = BabyPanda(col * SPRITE_SIZE, row_count * SPRITE_SIZE)
            self.tile_list.append(panda)
        elif tile == 8:
            ground = Ground(col * SPRITE_SIZE, row_count * SPRITE_SIZE)
            self.tile_list.append(ground)

