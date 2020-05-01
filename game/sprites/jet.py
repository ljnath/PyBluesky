import pygame
import math
from .bullet import Bullet

# Jet class which holds jet attributes and behaviour
class Jet(pygame.sprite.Sprite):
    """ Jet sprite class for creating and updating the jet in the game screen
    """
    def __init__(self, game_env):
        super(Jet, self).__init__()                                 # initilizing parent class pygame.sprite.Sprite
        self.__speed = 5                                            # setting jet speed as 5
        self.__game_env = game_env
        self.surf = pygame.image.load(game_env.constants.jet_image).convert()    # loading jet image from file;  image source https://www.flaticon.com/authors/iconixar
        self.surf.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL)           # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.rect = self.surf.get_rect(center=(50,self.__game_env.constants.screen_height/2)) # getting rectangle from jet screen; setting the jet position as the middle of the scrren on the left

    def update(self, pressed_keys):
        if pressed_keys[self.__game_env.K_UP]:                                  # if the UP key is pressed
            self.rect.move_ip(0, -self.__speed)                                 # moving the jet on negtaive y-axis
            self.__game_env.variables.moveup_sound.play()                       # playing the move_up sound
        if pressed_keys[self.__game_env.K_DOWN]:                                # if the DOWN key is pressed
            self.rect.move_ip(0, self.__speed)                                  # moving the jet on positive y-axis
            self.__game_env.variables.movedown_sound.play()                     # playing the move_down souund
        if pressed_keys[self.__game_env.K_LEFT]:                                # if the LEFT key is presssed
            self.rect.move_ip(-self.__speed, 0)                                 # moving the jet on negative x-axis
        if pressed_keys[self.__game_env.K_RIGHT]:                               # if the RIGHT key is pressed
            self.rect.move_ip(self.__speed, 0)                                  # moving the jet on positive x-axis

        if self.rect.left < 0: self.rect.left = 0                               # if the jet has moved left and have crossed the screen; the left position is set to 0 as it is the boundary
        if self.rect.top < 0: self.rect.top = 0                                 # if the jet has moved top and have crossed the screen; the top position is set to 0 as it is the boundary
        if self.rect.right > self.__game_env.constants.screen_width:
            self.rect.right = self.__game_env.constants.screen_width            # if the jet has moved right and have crossed the screen; the right position is set to screen width as it is the boundary
        if self.rect.bottom > self.__game_env.constants.screen_height:
            self.rect.bottom = self.__game_env.constants.screen_height          # if the jet has moved bottom and have crossed the screen; the bottom position is set to screen width as it is the boundary

    def auto_move(self, position):
        dx = position[0] - self.rect.x                                          # calculating x-coordinate difference of mouse and current jet position
        dy = position[1] - self.rect.y                                          # caluclating y-coordinate difference of mouse and current jet position
        angle = math.atan2(dy, dx)                                              # calculating angle
        if angle < 0:                                                           
            self.__game_env.variables.moveup_sound.play()                       # playing the move_up sound
        else:
            self.__game_env.variables.movedown_sound.play()                     # playing the move_up sound
        self.rect.x += self.__speed * math.cos(angle)                           # moving the x-coordinate of jet towards the mouse cursor
        self.rect.y += self.__speed * math.sin(angle)                           # moving the y-coordinate of jet towards the mouse cursor

    def shoot(self):
        if self.__game_env.variables.ammo > 0:
            bullet = Bullet(self.__game_env, self.rect.x+self.rect.width, self.rect.y+22)           # create a bullet where the jet is located
            self.__game_env.variables.bullets.add(bullet)                                           # add the bullet to bullet group
            self.__game_env.variables.all_sprites.add(bullet)                                       # add the bullet tp all_sprites
            self.__game_env.variables.shoot_sound.play()                                            # play shooting sound
            self.__game_env.variables.ammo -= 1
        else:
            self.__game_env.variables.all_sprites.add(self.__game_env.variables.noammo_sprite)      # show noammo sprite

