# Import the pygame module
import pygame
import random
import time
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)                               # loading constants from pygame.locals

__version__ = 0.2               # setting game version
__name__ = 'Bluesky'            # setting game name    


# Define a Text class for creating surface with custome text, size and color
class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color):
        pygame.sprite.Sprite.__init__(self)                                     # initializing parent class
        self.color = color                                                      # storing argument color in class variable
        self.font = pygame.font.Font('font/ARCADE.ttf', size)                   # loading font and creating class variable font with given size
        self.surf = self.font.render(text, 1, self.color)                       # creating surface by rendering the text
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))# creating rectangle from the surface
    
    def render(self, text):
        self.surf = self.font.render(text, 2, self.color)                       # dynamically updating the surface with updated text


# Define a ScoreBoard class object by Text class
class ScoreBoard(Text):
    def __init__(self):
        Text.__init__(self, text="TIME 0 SCORE 0", size=28, color=(255,255,255))                # initializing parent class with defautl text and color
        self.rect = self.surf.get_rect(topright=(SCREEN_WIDTH-5-self.surf.get_width() / 2, 2))  # creating rectangle from text surface
    
    def update(self, playtime, score):
        length = 5                                                                              # setting max length of score
        self.surf = self.font.render("TIME {} SCORE {}".format(str(playtime).zfill(length), str(score).zfill(length)), 1, self.color)   # updating scoreboard score and time


# Define a Cloud class object by extending pygame.sprite.Sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()                                               # initilizing parent class pygame.sprite.Sprite
        random_cloud = random.choice(('cloud1.png', 'cloud2.png', 'cloud3.png'))    # getting a random cloud image
        self.surf = pygame.image.load('image/{}'.format(random_cloud)).convert()    # loading cloud image
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)                           # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        x_pos = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)               # generating random x position for the cloud
        y_pos = random.randint(0, SCREEN_HEIGHT)                                    # generating random y position for the cloud
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))                       # create rectange from the cloud screen

    def update(self):
        self.rect.move_ip(-5, 0)                                        # move the cloud towards left at constant speed
        if self.rect.right < 0:                                         # if the cloud has completly moved from the screen, the cloud is killed
            self.kill()


# Missile class which holds missile attributes and behaviour
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile, self).__init__()                                 # initilizing parent class pygame.sprite.Sprite
        self.surf = pygame.image.load('image/missile.png').convert()    # loading missile image from file
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)               # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.speed = random.randint(5, 20)                              # generating random speed for the missle
        x_pos = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)   # generating random x position for the missile
        y_pos = random.randint(0, SCREEN_HEIGHT)                        # generating random y position for the missile
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))           # create rectange from the missile screen

    def update(self):
        self.rect.move_ip(-self.speed, 0)                               # move the missle towards left at the predefine speed
        if self.rect.right < 0:                                         # if the missile has completly moved from the screen, the missile is killed
            self.kill()


# Jet class which holds jet attributes and behaviour
class Jet(pygame.sprite.Sprite):
    def __init__(self):
        super(Jet, self).__init__()                                 # initilizing parent class pygame.sprite.Sprite
        self.surf = pygame.image.load('image/jet.png').convert()    # loading jet image from file;  image source https://www.flaticon.com/authors/iconixar
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)           # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.rect = self.surf.get_rect(center=(25,SCREEN_HEIGHT/2)) # getting rectangle from jet screen; setting the jet position as the middle of the scrren on the left

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:                                      # if the UP key is pressed
            self.rect.move_ip(0, -5)                                # moving the jet on negtaive y-axis
            move_up_sound.play()                                    # playing the move_up sound
        if pressed_keys[K_DOWN]:                                    # if the DOWN key is pressed
            self.rect.move_ip(0, 5)                                 # moving the jet on positive y-axis
            move_down_sound.play()                                  # playing the move_down souund
        if pressed_keys[K_LEFT]:                                    # if the LEFT key is presssed
            self.rect.move_ip(-5, 0)                                # moving the jet on negative x-axis
        if pressed_keys[K_RIGHT]:                                   # if the RIGHT key is pressed
            self.rect.move_ip(5, 0)                                 # moving the jet on positive x-axis

        if self.rect.left < 0: self.rect.left = 0                               # if the jet has moved left and have crossed the screen; the left position is set to 0 as it is the boundary
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH       # if the jet has moved right and have crossed the screen; the right position is set to screen width as it is the boundary
        if self.rect.top <= 0: self.rect.top = 0                                # if the jet has moved top and have crossed the screen; the top position is set to 0 as it is the boundary
        if self.rect.bottom >= SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT  # if the jet has moved bottom and have crossed the screen; the bottom position is set to screen width as it is the boundary


pygame.mixer.init()                                     # initializing same audio mixer with default settings
pygame.init()                                           # initializing pygame

running = True                                          # game running variable
clock = pygame.time.Clock()                             # setting up game clock to maintain constant fps
SCREEN_WIDTH = 800                                      # setting width of game screen
SCREEN_HEIGHT = 600                                     # setting height of game screen

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # creating game screen with custom width and height
pygame.display.set_caption('{} v{}'.format(__name__, __version__))  # setting name of game window

ADD_MISSILE = pygame.USEREVENT + 1                      # creating custom event to automatically add missiles in the screen
pygame.time.set_timer(ADD_MISSILE, 500)                 # setting event to auto-trigger every 500ms; 2 missiles will be created every second

ADD_CLOUD = pygame.USEREVENT + 2                        # creating custom event to automatically add cloud in the screen
pygame.time.set_timer(ADD_CLOUD, 1000)                  # setting event to auto-trigger every 1s; 1 cloud will be created every second

pygame.mixer.music.load("audio/Apoxode_-_Electric_1.mp3")# setting main game background music; Sound source: http://ccmixter.org/files/Apoxode/59262 | License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.play(loops=-1)                        # lopping the main game music

move_up_sound = pygame.mixer.Sound("audio/Rising_putter.ogg")       # creating move_up sound for jet movement; Sound sources: Jon Fincher
move_down_sound = pygame.mixer.Sound("audio/Falling_putter.ogg")    # creating move_down sound for jet movement; Sound sources: Jon Fincher
collision_sound = pygame.mixer.Sound("audio/collision.ogg")         # creating collision sound for jet collision

move_up_sound.set_volume(0.5)                           # setting half volume of move_up sound
move_down_sound.set_volume(0.5)                         # setting half volume of move_down sound
collision_sound.set_volume(2)                           # setting double volume of collision sound

jet = Jet()                                             # creating the jet for the game
scoreBoard = ScoreBoard()                               # creating the scoreboard for the game
all_sprites = pygame.sprite.Group()                     # creating group of sprites to hold all the srites in the game
all_sprites.add(jet)                                    # adding the jet to all_sprites
all_sprites.add(scoreBoard)                             # adding the scoreboard to all_sprites

clouds = pygame.sprite.Group()                          # creating cloud group for storing all the clouds in the game
missiles = pygame.sprite.Group()                        # creating missile group for storing all teh missiles in the game
score = 0                                               # default score
playtime = 0                                            # default game score

exit_delay = False

# Main game loop
while running:
    for event in pygame.event.get():                                                # Look at every event in the queue
        if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:   # stopping game when ESC key is pressed or when the game window is closed
            running = False
        elif event.type == ADD_MISSILE:                 # is event to add missile is triggered
            new_missile = Missile()                     # create a new missile
            missiles.add(new_missile)                   # adding the missile to missle group
            all_sprites.add(new_missile)                # adding the missile to all_sprites group as well
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()                         # is event to add cloud is triggered
            clouds.add(new_cloud)                       # create a new cloud
            all_sprites.add(new_cloud)                  # adding the cloud to all_sprites group
            playtime += 1                               # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
            score += 10                                 # increasing score by 10 as this event is triggered every second

    
    screen.fill((135, 206, 250))                        # Filling screen with sky blue color
    [screen.blit(sprite.surf, sprite.rect) for sprite in all_sprites]       # drawing all sprites in the screen

    if pygame.sprite.spritecollideany(jet, missiles):   # Check if any missiles have collided with the player; if so
        jet.kill()                                      # killing the jet
        move_up_sound.stop()                            # stopping any move_up sound
        move_down_sound.stop()                          # stopping any move_down sound
        collision_sound.play()                          # playing collision sound

        message = Text("GAME OVER", 60, (255, 0, 0))    # creating game over message
        screen.blit(message.surf, message.rect)         # adding message
        running = False                                 # stopping game
        exit_delay = True

    pygame.display.flip()                               # updating display to the screen
    clock.tick(30)                                      # ticking game clock at 30 to maintain 30fps

    pressed_keys = pygame.key.get_pressed()             # getting all the pressed keys
    jet.update(pressed_keys)                            # calling update() to act according to pressed keys

    missiles.update()                                   # update the position of the missiles
    clouds.update()                                     # update the postition of the clouds
    scoreBoard.update(playtime, score)                  # update the game score board

    if exit_delay:
        time.sleep(2)

pygame.mixer.music.stop()                               # stopping game music
pygame.mixer.quit()                                     # stopping game sound mixer