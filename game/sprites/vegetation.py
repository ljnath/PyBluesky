from pygame import sprite, image, transform
import random
import math
class Vegetation(sprite.Sprite):
    """ Vegetation sprite class for creating and updating the vegetation in the game screen
    """
    def __init__(self, game_env, x_pos=None, y_pos=None):
        super(Vegetation, self).__init__()
        self.__game_env= game_env
        self.surf = image.load(random.choice(self.__game_env.static.vegetation)).convert()
        ground = image.load(self.__game_env.static.ground).convert()
        grass = image.load(self.__game_env.static.grass).convert()
        grass.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL) 

        pos = 0
        for _ in range(math.ceil(self.surf.get_width() / ground.get_width())):
            self.surf.blit(ground, (pos, self.surf.get_height() - 40))
            if random.choice([0,1]) == 0:
                self.surf.blit(grass, (pos-38, self.surf.get_height() -40-32))
            pos += ground.get_width()

        
        x_pos = self.__game_env.static.screen_width if x_pos is None else x_pos
        y_pos = self.__game_env.static.screen_height - self.surf.get_height() / 2 if y_pos is None else y_pos
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))
        self.__speed = 2

    def update(self):
        self.rect.move_ip(-self.__speed, 0)
        if self.rect.right < 0:
            self.kill()
