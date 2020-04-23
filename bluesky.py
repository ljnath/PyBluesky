# Import the pygame module
import pygame
import random
import time

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define a Text class for creating surface with custome text, size and color
class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.font = pygame.font.Font('font/ARCADE.ttf', size)
        self.surf = self.font.render(text, 1, self.color)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    def render(self, text):
        self.surf = self.font.render(text, 2, self.color)


# Define a ScoreBoard class, a subclass of Text to display the score in screen
class ScoreBoard(Text):
    def __init__(self):
        self.max_length = 5
        Text.__init__(self, text="TIME 0 SCORE 0", size=28, color=(255,255,255))
        self.rect = self.surf.get_rect(topright=(SCREEN_WIDTH - 5 - self.surf.get_width() / 2, 2))
    
    def update(self, second, score):
        self.surf = self.font.render("TIME {} SCORE {}".format(str(second).zfill(self.max_length), str(score).zfill(self.max_length)), 1, self.color)


# Define a Cloud class object by extending pygame.sprite.Sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('image/cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT) 
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Define a Jet class object by extending pygame.sprite.Sprite
class Jet(pygame.sprite.Sprite):
    def __init__(self):
        super(Jet, self).__init__()
        self.surf = pygame.image.load('image/jet.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center = (25, SCREEN_HEIGHT/2))

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define a Missile class object by extending pygame.sprite.Sprite
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile, self).__init__()
        self.surf = pygame.image.load('image/missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bluesky v0.1')

# Create a custom event for adding a new enemy
ADD_MISSILE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_MISSILE, 500)

ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

# UPDATE_SCORE = pygame.USEREVENT + 3
# pygame.time.set_timer(UPDATE_SCORE, 3000)

# Variable to keep the main loop running
running = True
exit_delay = False

jet = Jet()
scoreBoard = ScoreBoard()

# Create groups to hold enemy sprites and all sprites
# - missiles is used for collision detection and position updates
# - all_sprites is used for rendering
clouds = pygame.sprite.Group()
missiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jet)
all_sprites.add(scoreBoard)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("audio/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("audio/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("audio/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("audio/Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

score = 0
playtime = 0

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Add a new missile?
        elif event.type == ADD_MISSILE:
            # Create the new missile and add it to sprite groups
            new_missile = Missile()
            missiles.add(new_missile)
            all_sprites.add(new_missile)

        # Add a new cloud?
        elif event.type == ADD_CLOUD:
            # Create the new enemy and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

            # increasing playtime by 1s as this event is triggered every second
            playtime += 1
            # increasing score by 10 as this event is triggered every second
            score += 10

    # Fill the screen with white
    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any missiles have collided with the player
    if pygame.sprite.spritecollideany(jet, missiles):
        # If so, then remove the player and stop the loop
        jet.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        message = Text("GAME OVER", 60, (255, 0, 0))
        screen.blit(message.surf, message.rect)
        running = False
        exit_delay = True

    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    jet.update(pressed_keys)

    missiles.update()
    clouds.update()
    scoreBoard.update(playtime, score)

    if exit_delay:
        time.sleep( 3)

pygame.mixer.music.stop()
pygame.mixer.quit()