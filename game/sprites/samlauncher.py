import math
import random

from game.environment import GameEnvironment
from game.sprites.sam import Sam
from pygame import image, sprite, transform


class SamLauncher(sprite.Sprite):
    """ SamLauncher sprite class for creating and updating the vegetation in the game screen
    """
    def __init__(self):
        super(SamLauncher, self).__init__()
        self.__game_env= GameEnvironment()
        self.surf = image.load(self.__game_env.static.sam_launcher).convert()
        self.surf.set_colorkey((255,255,255), self.__game_env.RLEACCEL) 
        self.__speed = random.randint(8,12)                                 # speed of the sam launcher
        self.__flip = random.choice([True, False])                          # random filp choice, filp-launcher will travel from left2right, else from right2left
        self.__fired = False if random.choice([0,1,2]) == 0 else True     # random choice is the launcher will fire or not; reducing launch probabity to 25%
        self.__min_distance = int(random.randint(10,30) * self.__game_env.static.screen_width / 100)  # min distance to cover before the launcher can fire

        # flip logic
        if self.__flip:
            self.surf = transform.flip(self.surf, True, False)
            x_pos = 0
        else:
            x_pos = self.__game_env.static.screen_width
            self.__speed *= -1
            self.__min_distance -= self.__game_env.static.screen_width

        y_pos = self.__game_env.static.screen_height - self.surf.get_height() - 15
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))
        
    def update(self, target):
        if not self.__fired and self.rect.x > self.__min_distance:    # if not fired and if the launcher has crossed the minimum diatance
            self.fire(target)
            self.__fired = True

        self.rect.move_ip(self.__speed, 0)
        if self.rect.right < 0 or self.rect.left > self.__game_env.static.screen_width:
            self.kill()

    def fire(self, target):
        sam = Sam((self.rect.x, self.rect.y), target, self.__flip)
        self.__game_env.dynamic.sam_missiles.add(sam)
        self.__game_env.dynamic.all_sprites.add(sam)
        self.__game_env.dynamic.samfire_sound.play()
