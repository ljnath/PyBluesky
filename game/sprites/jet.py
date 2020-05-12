import math

from pygame import image, sprite

from game.data.enums import InputMode

from .bullet import Bullet


# Jet class which holds jet attributes and behaviour
class Jet(sprite.Sprite):
    """ Jet sprite class for creating and updating the jet in the game screen
    """
    def __init__(self, game_env):
        super(Jet, self).__init__()                                                             # initilizing parent class pygame.sprite.Sprite
        self.__game_env = game_env
        self.__speed = 7 if self.__game_env.dynamic.game_input == InputMode.KEYBOARD else 9     # setting jet speed as 7 in keyboard and 9 in mouse mode
        self.surf = image.load(game_env.static.jet_image).convert()                             # loading jet image from file
        self.surf.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL)                       # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.rect = self.surf.get_rect(center=(50,self.__game_env.static.screen_height/2))      # getting rectangle from jet screen; setting the jet position as the middle of the scrren on the left

    def update(self, pressed_keys):
        if pressed_keys[self.__game_env.K_UP]:                                  # if the UP key is pressed
            self.rect.move_ip(0, -self.__speed)                                 # moving the jet on negtaive y-axis
        if pressed_keys[self.__game_env.K_DOWN]:                                # if the DOWN key is pressed
            self.rect.move_ip(0, self.__speed)                                  # moving the jet on positive y-axis
        if pressed_keys[self.__game_env.K_LEFT]:                                # if the LEFT key is presssed
            self.rect.move_ip(-self.__speed, 0)                                 # moving the jet on negative x-axis
        if pressed_keys[self.__game_env.K_RIGHT]:                               # if the RIGHT key is pressed
            self.rect.move_ip(self.__speed, 0)                                  # moving the jet on positive x-axis

        self.__maintain_boundary()

    def auto_move(self, position):
        dx = position[0] - self.rect.x                                                                              # calculating x-coordinate difference of mouse and current jet position
        dy = position[1] - self.rect.y                                                                              # caluclating y-coordinate difference of mouse and current jet position
        if (dx >= -self.__speed and dx <= self.__speed) and (dy >= -self.__speed and dy <= self.__speed):           # jet will not move if the delta is less then its speed
            return
        angle = math.atan2(dy, dx)                                                                                  # calculating angle
        self.rect.x += self.__speed * math.cos(angle)                                                               # moving the x-coordinate of jet towards the mouse cursor
        self.rect.y += self.__speed * math.sin(angle)                                                               # moving the y-coordinate of jet towards the mouse cursor
        self.__maintain_boundary()

    def shoot(self):
        if self.__game_env.dynamic.ammo > 0:
            bullet = Bullet(self.__game_env, self.rect.x+self.rect.width+10, self.rect.y+22)      # create a bullet where the jet is located
            self.__game_env.dynamic.bullets.add(bullet)                                           # add the bullet to bullet group
            self.__game_env.dynamic.all_sprites.add(bullet)                                       # add the bullet tp all_sprites
            self.__game_env.dynamic.shoot_sound.play()                                            # play shooting sound
            self.__game_env.dynamic.ammo -= 1
            self.__game_env.dynamic.bullets_fired += 1
        else:
            self.__game_env.dynamic.all_sprites.add(self.__game_env.dynamic.noammo_sprite)      # show noammo sprite

    def __maintain_boundary(self):
        if self.rect.left < 0: self.rect.left = 0                               # if the jet has moved left and have crossed the screen; the left position is set to 0 as it is the boundary
        if self.rect.top < 0: self.rect.top = 0                                 # if the jet has moved top and have crossed the screen; the top position is set to 0 as it is the boundary
        if self.rect.right > self.__game_env.static.screen_width:
            self.rect.right = self.__game_env.static.screen_width            # if the jet has moved right and have crossed the screen; the right position is set to screen width as it is the boundary
        if self.rect.bottom > self.__game_env.static.screen_height - self.__game_env.vegetation_size[1]/2:
            self.rect.bottom = self.__game_env.static.screen_height - self.__game_env.vegetation_size[1]/2   # if the jet has moved bottom and have crossed the screen; the bottom position is set to screen width as it is the boundary
