# Import the pygame module
import pygame
import random
import math
from enum import Enum

from pygame.locals import (
    SRCALPHA,
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    MOUSEMOTION,
    FULLSCREEN,
    QUIT,
)                               # loading constants from pygame.locals

__version__ = 0.5               # setting game version
__name__ = 'Bluesky'            # setting game name    

# enum defining the available input mode
class InputMode(Enum):
    KEYBOARD = 1,
    MOUSE = 2


# Define a Text class for creating surface with custome text, size and color
class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, x_pos=None, y_pos=None):
        pygame.sprite.Sprite.__init__(self)                                     # initializing parent class
        self.color = color                                                      # storing argument color in class variable
        self.font = pygame.font.Font('font/ARCADE.ttf', size)                   # loading font and creating class variable font with given size
        self.surf = self.font.render(text, 1, self.color)                       # creating surface by rendering the text
        if not x_pos:
            x_pos = SCREEN_WIDTH/2
        if not y_pos:
            y_pos = SCREEN_HEIGHT/2
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))                  # creating rectangle from the surface
    
    def render(self, text):
        self.surf = self.font.render(text, 2, self.color)                       # dynamically updating the surface with updated text


# Define a ScoreBoard class object by Text class
class ScoreBoard(Text):
    def __init__(self):
        Text.__init__(self, text="TIME 0 SCORE 0", size=28, color=(255,255,255))                # initializing parent class with defautl text and color
        self.rect = self.surf.get_rect(topright=(SCREEN_WIDTH-10-self.surf.get_width() / 2, 2))  # creating rectangle from text surface
    
    def update(self, playtime, score):
        length = 5                                                                              # setting max length of score
        self.surf = self.font.render("TIME {} SCORE {}".format(str(playtime).zfill(length), str(score).zfill(length)), 1, self.color)   # updating scoreboard score and time


# ReplaySprite class for drawing the replay game messages 
class ReplaySprite(Text):
    def __init__(self): 
        Text.__init__(self, text='', size=38, color=(255,0,0))                  # initilizing parent class with default text color as red
        highlight_color = (0,0,255)                                             # setting the text highlight color as blue
        self.__prefix_surf = self.font.render("Replay ", 1, self.color)         # creating surface with the Replay text
        self.__y_surf_highlight = self.font.render("Yes", 1, highlight_color)   # creating surface with Yes text when highlighted
        self.__n_surf = self.font.render("/No",1, self.color)                   # creating surface with No text
        self.__y_surf = self.font.render("Yes/", 1, self.color)                 # creating surface with Yes text
        self.__n_surf_highlight = self.font.render("No",1, highlight_color)     # creating surface with No text when highlighted
        self.__highlightY()                                                     # calling method to highlight Yes (the default choice)
        self.replayGame = True                                                  # setting replay to True
        
    def __recreateSurf(self):
        # creating default surface of combination of expected length
        self.surf = pygame.surface.Surface((self.__prefix_surf.get_width() + self.__y_surf.get_width() + self.__n_surf.get_width(), self.__prefix_surf.get_height()), SRCALPHA)
        self.surf.blit(self.__prefix_surf, (0,0))                                                               # updating the surface by drawing the prefex surface

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:                                                # checking if user has pressed LEFT
            self.replayGame = True                                              # setting game replay choice as True
            self.__highlightY()                                                 # calling method to highlight Yes
        elif pressed_keys[K_RIGHT]:                                             # checking if user has pressed RIGHT
            self.replayGame = False                                             # setting game replay choice as False
            self.__highlightN()                                                 # calling method to highlight No
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10))   # creating default rect and setting its position center below the GAME OVER text

    def __highlightY(self):
        self.__recreateSurf()
        self.surf.blit(self.__y_surf_highlight, (self.__prefix_surf.get_width(),0))                             # updating the surface by drawing the highlighted Yes after the prefix
        self.surf.blit(self.__n_surf, (self.__prefix_surf.get_width() + self.__y_surf_highlight.get_width(),0)) # updating the surface by drawing the No after the highlighted Yes

    def __highlightN(self):
        self.__recreateSurf()
        self.surf.blit(self.__y_surf, (self.__prefix_surf.get_width(),0))                                       # updating the surface by drawing the Yes after the prefix
        self.surf.blit(self.__n_surf_highlight, (self.__prefix_surf.get_width() + self.__y_surf.get_width(),0)) # updating the surface by drawing the highlighted No after the Yes


# GameInput class for drawing the replay game messages 
class GameInput(Text):
    def __init__(self): 
        Text.__init__(self, text='', size=48, color=(255,0,0))                          # initilizing parent class with default text color as red
        highlight_color = (0,0,255)                                                     # setting the text highlight color as blue
        self.__jet = Jet()                                                              # creating a of jet 
        self.__prefix_surf = self.font.render('Choose input mode', 1, self.color)       # creating surface with the prefix text
        self.__mouse = self.font.render(' Mouse',1, self.color)                         # creating surface with mouse text
        self.__keybrd = self.font.render(' Keyboard', 1, self.color)                    # creating surface with mouse text

        keybrd_surf = self.font.render(' Keyboard', 1, highlight_color)                 # creating surface with Keyboard text when highlighted
        self.__keybrd_highlighed = pygame.surface.Surface((self.__jet.surf.get_width() + keybrd_surf.get_width(), keybrd_surf.get_height()), SRCALPHA)     # creating surface for jet and highlighted keyboard text
        self.__keybrd_highlighed.blit(self.__jet.surf, (0,0))                           # drawing the jet
        self.__keybrd_highlighed.blit(keybrd_surf, (self.__jet.surf.get_width(), 0))    # drawing the highligted keyboard text after the jet image 
        
        mouse_surf = self.font.render(' Mouse', 1, highlight_color)                     # creating surface with mouse text when highlighted
        self.__mouse_highlighed = pygame.surface.Surface((self.__jet.surf.get_width() + mouse_surf.get_width(), mouse_surf.get_height()), SRCALPHA)       # creating surface for jet and highlighted mouse text
        self.__mouse_highlighed.blit(self.__jet.surf, (0,0))                            # drawing the jet
        self.__mouse_highlighed.blit(mouse_surf, (self.__jet.surf.get_width(), 0))      # drawing the highligted mouse text after the jet image 

        self.__highlightKeyboard()                                                      # calling method to highlight keyboard (the default choice)
        self.userChoice = InputMode.KEYBOARD
        
    def __recreateSurf(self):
        self.surf = pygame.surface.Surface((self.__prefix_surf.get_width(), self.__prefix_surf.get_height() * 3), SRCALPHA) # creating default surface of combinted expected length
        self.surf.blit(self.__prefix_surf, (0,0))                                                                           # drawing the prefix text

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:                                                          # checking if user has pressed UP
            self.userChoice = InputMode.KEYBOARD                                        # setting game input mode as keyboard
            self.__highlightKeyboard()                                                  # calling method to highlight keyboard
        elif pressed_keys[K_DOWN]:                                                      # checking if user has pressed DOWN
            self.userChoice = InputMode.MOUSE                                           # setting game input mode as mouse
            self.__highlightMouse()                                                     # calling method to highlight mouse
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))        # creating default rect and setting its position center

    def __highlightKeyboard(self):
        self.__recreateSurf()                                                           # recreating the surface, as we will re-draw
        self.surf.blit(self.__keybrd_highlighed, (0,self.__prefix_surf.get_height()))   # drawing the jet+keyboard text
        self.surf.blit(self.__mouse, (self.__jet.surf.get_width(), self.__prefix_surf.get_height() * 2))          # drawing the mouse text

    def __highlightMouse(self):
        self.__recreateSurf()                                                           # recreating the surface, as we will re-draw
        self.surf.blit(self.__keybrd, (self.__jet.surf.get_width(), self.__prefix_surf.get_height()))             # drawing keyboard text
        self.surf.blit(self.__mouse_highlighed, (0, self.__prefix_surf.get_height()*2)) # drawing jet+mouse text


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
        self.__speed = 5                                            # setting jet speed as 5
        self.surf = pygame.image.load('image/jet.png').convert()    # loading jet image from file;  image source https://www.flaticon.com/authors/iconixar
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)           # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.rect = self.surf.get_rect(center=(50,SCREEN_HEIGHT/2)) # getting rectangle from jet screen; setting the jet position as the middle of the scrren on the left

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:                                                  # if the UP key is pressed
            self.rect.move_ip(0, -self.__speed)                                 # moving the jet on negtaive y-axis
            move_up_sound.play()                                                # playing the move_up sound
        if pressed_keys[K_DOWN]:                                                # if the DOWN key is pressed
            self.rect.move_ip(0, self.__speed)                                  # moving the jet on positive y-axis
            move_down_sound.play()                                              # playing the move_down souund
        if pressed_keys[K_LEFT]:                                                # if the LEFT key is presssed
            self.rect.move_ip(-self.__speed, 0)                                 # moving the jet on negative x-axis
        if pressed_keys[K_RIGHT]:                                               # if the RIGHT key is pressed
            self.rect.move_ip(self.__speed, 0)                                 # moving the jet on positive x-axis

        if self.rect.left < 0: self.rect.left = 0                               # if the jet has moved left and have crossed the screen; the left position is set to 0 as it is the boundary
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH       # if the jet has moved right and have crossed the screen; the right position is set to screen width as it is the boundary
        if self.rect.top <= 0: self.rect.top = 0                                # if the jet has moved top and have crossed the screen; the top position is set to 0 as it is the boundary
        if self.rect.bottom >= SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT  # if the jet has moved bottom and have crossed the screen; the bottom position is set to screen width as it is the boundary
    
    def move(self, position):
        dx = position[0] - self.rect.x                                          # calculating x-coordinate difference of mouse and current jet position
        dy = position[1] - self.rect.y                                          # caluclating y-coordinate difference of mouse and current jet position
        angle = math.atan2(dy, dx)                                              # calculating angle
        if angle < 0:                                                           
            move_up_sound.play()                                                # playing the move_up sound
        else:
            move_down_sound.play()                                              # playing the move_up sound
        self.rect.x += self.__speed * math.cos(angle)                           # moving the x-coordinate of jet towards the mouse cursor
        self.rect.y += self.__speed * math.sin(angle)                           # moving the y-coordinate of jet towards the mouse cursor


pygame.mixer.init()                                                 # initializing same audio mixer with default settings
pygame.init()                                                       # initializing pygame

running = True                                                      # game running variable
gameclock = pygame.time.Clock()                                     # setting up game clock to maintain constant fps
FPS = 30                                                            # setting game fps as 30
SCREEN_WIDTH = 800                                                  # setting width of game screen
SCREEN_HEIGHT = 600                                                 # setting height of game screen
MISSILE_PER_SEC = 4                                                 # setting up the number of missiles per second
CLOUD_PER_SEC = 1                                                   # setting up the number of cloud per second
GAMEPLAY_SCREEN = (135, 206, 250)                                   # default game screen color, skyblue
GAMEOVER_SCREEN = (196, 226, 255)                                   # screen color during gameover, pale skyblue

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # creating game screen with custom width and height
pygame.display.set_caption('{} ver. {}'.format(__name__, __version__))# setting name of game window
pygame.mouse.set_visible(False)                                     # hiding the mouse pointer from the game screen

ADD_MISSILE = pygame.USEREVENT + 1                                  # creating custom event to automatically add missiles in the screen
pygame.time.set_timer(ADD_MISSILE, int(1000/MISSILE_PER_SEC))       # setting event to auto-trigger every 500ms; 2 missiles will be created every second

ADD_CLOUD = pygame.USEREVENT + 2                                    # creating custom event to automatically add cloud in the screen
pygame.time.set_timer(ADD_CLOUD, int(1000/CLOUD_PER_SEC))           # setting event to auto-trigger every 1s; 1 cloud will be created every second

pygame.mixer.music.load("audio/Apoxode_-_Electric_1.mp3")           # setting main game background music; Sound source: http://ccmixter.org/files/Apoxode/59262 | License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.play(loops=-1)                                   # lopping the main game music

move_up_sound = pygame.mixer.Sound("audio/Rising_putter.ogg")       # creating move_up sound for jet movement; Sound sources: Jon Fincher
move_down_sound = pygame.mixer.Sound("audio/Falling_putter.ogg")    # creating move_down sound for jet movement; Sound sources: Jon Fincher
collision_sound = pygame.mixer.Sound("audio/collision.ogg")         # creating collision sound for jet collision

move_up_sound.set_volume(0.5)                                       # setting half volume of move_up sound
move_down_sound.set_volume(0.5)                                     # setting half volume of move_down sound
collision_sound.set_volume(2)                                       # setting double volume of collision sound

mouse_position = (SCREEN_WIDTH, SCREEN_HEIGHT/2)                    # default mouse position, let the jet move forward on a straight line
gameover = False                                                    # no gameover by default
game_started = False                                                # game is not started by default
input_mode = InputMode.KEYBOARD                                     # default input mode is set to keyboard
score = 0                                                           # default score
playtime = 0                                                        # default game score
screen_color = GAMEOVER_SCREEN                                      # to store the current scrreen color; updating in case of gameover

replaySprite = ReplaySprite()                                       # creating replay text sprite
gameInput = GameInput()                                             # creating gameinput sprite
jet = Jet()                                                         # creating the jet for the game
scoreBoard = ScoreBoard()                                           # creating the scoreboard for the game

clouds = pygame.sprite.Group()                                      # creating cloud group for storing all the clouds in the game
missiles = pygame.sprite.Group()                                    # creating missile group for storing all teh missiles in the game
all_sprites = pygame.sprite.Group()                                 # creating group of sprites to hold all the srites in the game
all_sprites.add(gameInput)                                          # adding gameinput to all_sprites group to be drawn on the screen

def show_gameover():
    global screen_color, gameover                                   # updating global variable
    screen_color = GAMEOVER_SCREEN                                  # updating screen color to gameover one
    gameover = True                                                 # activating gameover
    gameover_txt = Text("GAME OVER", 60, (255,0,0), x_pos=SCREEN_WIDTH/2 - 10 ,y_pos = SCREEN_HEIGHT/2-25)        # creating game over message sprite
    all_sprites.add(gameover_txt)                                   # adding gameover text sprite to all_sprites for repetated rendereing incase of gameover
    all_sprites.add(replaySprite)                                   # adding replay text sprite to all_sprites for repetated rendereing incase of gameover


# Main game loop
while running:
    for event in pygame.event.get():                                                        # Look at every event in the queue
        if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:           # stopping game when ESC key is pressed or when the game window is closed
            running = False
        elif input_mode == input_mode.MOUSE and event.type == MOUSEMOTION and not gameover: # moving jet based on mouse movement
            mouse_position = pygame.mouse.get_pos()                                         # saving the mouse co-ordinate for smooth movement later
        elif not game_started and event.type == KEYDOWN and event.key == K_RETURN:
            input_mode = gameInput.userChoice                                               # getting the user input choice on RETURN press
            pygame.mouse.set_visible(True if input_mode == InputMode.MOUSE else False)      # displaying mouse cursor based on user input mode
            screen_color = GAMEPLAY_SCREEN                                                  # restoring screen colot
            game_started = True                                                             # starting game
            all_sprites.remove(gameInput)                                                   # removing the input selection sprite
            all_sprites.add(jet)                                                            # adding the jet to all_sprites
            all_sprites.add(scoreBoard)                                                     # adding the scoreboard to all_sprites
        elif gameover and event.type == KEYDOWN and event.key == K_RETURN and game_started: # checking for replay text only after the game is started
            if replaySprite.replayGame:
                gameover = False                                            # setting gameover variable to false as user as opted to replay
                jet = Jet()                                                 # re-creating the jet
                all_sprites = pygame.sprite.Group()                         # re-creating group of sprites 
                all_sprites.add(jet)                                        # adding the jet to all_sprites
                all_sprites.add(scoreBoard)                                 # adding the scoreboard to all_sprites
                clouds = pygame.sprite.Group()                              # re-creating cloud groups
                missiles = pygame.sprite.Group()                            # re-creating missile groups
                screen_color = GAMEPLAY_SCREEN                              # restoring  screen color
                score, playtime = 0, 0                                      # reseting game score and playtime
            else:
                running = False                                             # stopping game as user as opted not to replay
        elif game_started and event.type == ADD_MISSILE and not gameover:                    # is event to add missile is triggered; missles are not added during gameover
            new_missile = Missile()                                         # create a new missile
            missiles.add(new_missile)                                       # adding the missile to missle group
            all_sprites.add(new_missile)                                    # adding the missile to all_sprites group as well
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()                                             # is event to add cloud is triggered
            clouds.add(new_cloud)                                           # create a new cloud
            all_sprites.add(new_cloud)                                      # adding the cloud to all_sprites group
            if not gameover and game_started:
                playtime += 1                                               # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
                score += 10                                                 # increasing score by 10 as this event is triggered every second

    screen.fill(screen_color)                                               # Filling screen with sky blue color
    [screen.blit(sprite.surf, sprite.rect) for sprite in all_sprites]       # drawing all sprites in the screen

    if pygame.sprite.spritecollideany(jet, missiles):                       # Check if any missiles have collided with the player; if so
        jet.kill()                                                          # killing the jet
        move_up_sound.stop()                                                # stopping any move_up sound
        move_down_sound.stop()                                              # stopping any move_down sound
        collision_sound.play()                                              # playing collision sound
        show_gameover()                                                     # show gameover infomation as game as ended
        
    pygame.display.flip()                                                   # updating display to the screen
    gameclock.tick(FPS)                                                     # ticking game clock at 30 to maintain 30fps

    pressed_keys = pygame.key.get_pressed()                                 # getting all the pressed keys
    if game_started and not gameover and input_mode == InputMode.KEYBOARD:
        jet.update(pressed_keys)                                            # calling update() to act according to pressed keys
    elif game_started and gameover:
        replaySprite.update(pressed_keys)                                   # allowing user to select replay game choice during gameover mode
    elif not game_started:
        gameInput.update(pressed_keys)
    
    if game_started and not gameover and input_mode == InputMode.MOUSE:     # performing the jet movement here for smooth movement till mouse cursor
        jet.move(mouse_position)

    missiles.update()                                                       # update the position of the missiles
    clouds.update()                                                         # update the postition of the clouds
    scoreBoard.update(playtime, score)                                      # update the game score board

pygame.mixer.music.stop()                                                   # stopping game music
pygame.mixer.quit()                                                         # stopping game sound mixer