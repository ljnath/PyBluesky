"""
MIT License

Copyright (c) 2020 Lakhya Jyoti Nath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

PyBluesky - A simple python game to navigate your jet and fight though a massive missiles attack based on pygame framework

Version: 1.0.2
Author: Lakhya Jyoti Nath (ljnath)
Email:  ljnath@ljnath.com
Website: https://www.ljnath.com
"""

import pygame
import random
import math
from game.environment import GameEnvironment
from game.sprites.jet import Jet
from game.sprites.missile import Missile
from game.sprites.cloud import Cloud
from game.sprites.vegetation import Vegetation
from game.sprites.star import Star
from game.sprites.text import Text
from game.sprites.text.score import ScoreText
from game.sprites.text.replay import ReplayText
from game.sprites.text.gamemenu import GameMenuText
from game.sprites.text.help import HelpText
from game.sprites.text.leaderboard import LeaderBoardText
from game.sprites.text.input.name import NameInputText
from game.handlers.network import NetworkHandler
from game.handlers.leaderboard import LeaderBoardHandler
from game.data.enums import InputMode, Screen
from threading import Thread

API_KEY = ''

def load_leaders():
    leader_thread = Thread(target=LeaderBoardHandler().update, args=([API_KEY]))
    leader_thread.start()
    leader_thread.join()

def check_update(game_env):
    check_update_thread = Thread(target=NetworkHandler().check_game_update, args=([API_KEY, game_env]))
    check_update_thread.start()
    check_update_thread.join()
    load_leaders()

def submit_result(game_env):
    if game_env.dynamic.game_score > 0:
        network_thread = Thread(target=NetworkHandler().submit_result, args=([API_KEY, game_env]))
        network_thread.start()
        network_thread.join()
    load_leaders()

def create_vegetation(game_env, vegetations):
    vegetations.empty()
    for i in range(math.ceil(game_env.static.screen_width / game_env.vegetation_size[0])):                          # drawing the 1st vegetations required to fill the 1st sceen (max is the screen width)
        vegetation = Vegetation(game_env, x_pos= i * game_env.vegetation_size[0] + game_env.vegetation_size[0]/2)   # creating a new vegetation
        vegetations.add(vegetation)                                                                                 # just adding sprite to vegetations group, to updating on screen for now

def play():
    pygame.mixer.init()                                                 # initializing same audio mixer with default settings
    pygame.init()                                                       # initializing pygame
    game_env = GameEnvironment()                                        # initializing game environment

    game_env.dynamic.collision_sound.set_volume(1.5)
    game_env.dynamic.levelup_sound.set_volume(1.5)
    game_env.dynamic.shoot_sound.set_volume(1.5)
    game_env.dynamic.hit_sound.set_volume(3)
    game_env.dynamic.powerup_sound.set_volume(10)

    pygame.mixer.music.load(game_env.static.game_sound.get('music'))                                        # setting main game background musicm
    pygame.mixer.music.play(loops=-1)                                                                       # lopping the main game music
    pygame.mixer.music.set_volume(.3)

    # screen = pygame.display.set_mode((game_env.static.screen_width, game_env.static.screen_height))         # creating game screen with custom width and height
    screen = pygame.display.set_mode((game_env.static.screen_width, game_env.static.screen_height), game_env.FULLSCREEN)     # creating game screen with custom width and height
    pygame.display.set_caption('{} ver. {}'.format(game_env.static.name, game_env.static.version))          # setting name of game window
    pygame.display.set_icon(pygame.image.load(game_env.static.game_icon))                                   # updating game icon to the jet image
    pygame.mouse.set_visible(False)                                                     # hiding the mouse pointer from the game screen

    gameclock = pygame.time.Clock()                                                     # setting up game clock to maintain constant fps
    check_update(game_env)

    ADD_MISSILE = pygame.USEREVENT + 1                                                  # creating custom event to automatically add missiles in the screen
    pygame.time.set_timer(ADD_MISSILE, int(1000/game_env.static.missile_per_sec))       # setting event to auto-trigger every 500ms; 2 missiles will be created every second

    ADD_CLOUD = pygame.USEREVENT + 2                                                    # creating custom event to automatically add cloud in the screen
    pygame.time.set_timer(ADD_CLOUD, int(1000/game_env.static.cloud_per_sec))           # setting event to auto-trigger every 1s; 1 cloud will be created every second

    running = True                                                                      # game running variable
    gameover = False                                                                    # no gameover by default
    game_started = False                                                                # game is not started by default
    star_shown = False
    mouse_pos = (game_env.static.screen_width, game_env.static.screen_height/2)   # default mouse position, let the jet move forward on a straight line
    screen_color = game_env.static.background_default if game_started else game_env.static.background_special

    backgrounds = pygame.sprite.Group()                                                 # creating seperate group for background sprites
    stars = pygame.sprite.GroupSingle()                                                 # group of stars with max 1 sprite
    vegetations = pygame.sprite.Group()                                                 # creating cloud group for storing all the clouds in the game
    clouds = pygame.sprite.Group()                                                      # creating cloud group for storing all the clouds in the game
    missiles = pygame.sprite.Group()                                                    # creating missile group for storing all teh missiles in the game
    deactivated_missile = pygame.sprite.Group()                                         # creating missile group for storing all teh missiles in the game
    title_sprites = pygame.sprite.Group()

    general_hint_text = "Press M->Game menu, H->Help, L->LeaderBoard, ESC->Quit"
    active_sprite = NameInputText(game_env)
    hint_sprite = Text(game_env, "Enter your name and press [ENTER] or press [ESC] to quit", 22, pos_x=game_env.static.screen_width/2 , pos_y= 145)  # creating game help
    title_banner_sprite = Text(game_env, "{} {}".format(game_env.static.name, game_env.static.version), 100, pos_x=game_env.static.screen_width/2 , pos_y=100)                  # creating title_banner_sprite text sprite with game name
    title_author_sprite = Text(game_env, "Written by: Lakhya Jyoti Nath (www.ljnath.com)", 26, pos_x=game_env.static.screen_width/2 , pos_y= game_env.static.screen_height-20)  # creating game author

    if game_env.dynamic.player_name:
        hint_sprite = Text(game_env, general_hint_text, 22, pos_x=game_env.static.screen_width/2 , pos_y= 145)  # creating game help
        active_sprite = GameMenuText(game_env)

    game_env.dynamic.all_sprites.add(hint_sprite)
    [title_sprites.add(sprite) for sprite in (active_sprite, title_banner_sprite, title_author_sprite)]             # adding all the necessary sprites to title_sprites
    [game_env.dynamic.all_sprites.add(sprite) for sprite in title_sprites]                                          # adding all title_sprites sprite to all_sprites
        
    jet = Jet(game_env)                                                                                             # creating jet sprite
    scoretext_sprite = ScoreText(game_env)                                                                          # creating scoreboard sprite
    game_env.dynamic.noammo_sprite = Text(game_env, "NO AMMO !", 24)                                                # creating noammo-sprite 

    create_vegetation(game_env, vegetations)

    # Main game loop
    while running:
        for event in pygame.event.get():                                                                            # Look at every event in the queue
            if event.type == game_env.KEYDOWN and event.key == game_env.K_ESCAPE or event.type == game_env.QUIT:    # stopping game when ESC key is pressed or when the game window is closed
                running = False
            elif game_started and not gameover:
                if game_env.dynamic.game_input ==  InputMode.MOUSE and event.type == game_env.MOUSEMOTION:          # moving jet based on mouse movement
                    mouse_pos = pygame.mouse.get_pos()                                                              # saving the mouse co-ordinate for smooth movement later
                elif (game_env.dynamic.game_input ==  InputMode.KEYBOARD and event.type == game_env.KEYDOWN and event.key == game_env.K_SPACE) or (game_env.dynamic.game_input ==  InputMode.MOUSE and event.type==game_env.MOUSEBUTTONDOWN):
                    jet.shoot()
                if event.type == ADD_MISSILE:                                                                       # is event to add missile is triggered; missles are not added during gameover
                    new_missile = Missile(game_env)                                                                 # create a new missile
                    missiles.add(new_missile)                                                                       # adding the missile to missle group
                    game_env.dynamic.all_sprites.add(new_missile)                                                   # adding the missile to all_sprites group as well
            elif event.type == game_env.KEYDOWN:                                                                    # handling all the VALID key press, action varies based on current active screen
                if not game_started and game_env.dynamic.active_screen == Screen.NAMEINPUT:
                    active_sprite.render(event.unicode)
                    if game_env.dynamic.player_name:                                                                # if user has entered the name, then gamemenu is shown
                        [game_env.dynamic.all_sprites.remove(sprite) for sprite in (active_sprite, hint_sprite)]
                        active_sprite = GameMenuText(game_env)
                        hint_sprite = Text(game_env, general_hint_text, 22, pos_x=game_env.static.screen_width/2 , pos_y= 145)
                        [game_env.dynamic.all_sprites.add(sprite) for sprite in (active_sprite, hint_sprite)]
                        game_env.dynamic.active_screen = Screen.GAMEMENU
                        
                elif event.key == game_env.K_h and game_env.dynamic.active_screen != Screen.HELP:                   # displyaing the help menu
                    game_env.dynamic.all_sprites.remove(active_sprite)
                    active_sprite = HelpText(game_env)
                    game_env.dynamic.all_sprites.add(active_sprite)
                    game_env.dynamic.active_screen = Screen.HELP
                elif event.key == game_env.K_l and game_env.dynamic.active_screen != Screen.LEADERBOARD:            # displyaing the leaderboard
                    game_env.dynamic.all_sprites.remove(active_sprite)
                    active_sprite = LeaderBoardText(game_env)
                    game_env.dynamic.all_sprites.add(active_sprite)
                    game_env.dynamic.active_screen = Screen.LEADERBOARD
                elif event.key == game_env.K_m:
                    game_env.dynamic.all_sprites.remove(active_sprite)
                    if not gameover and game_env.dynamic.active_screen != Screen.GAMEMENU:                     # displyaing the game menu
                        active_sprite = GameMenuText(game_env)
                        game_env.dynamic.active_screen = Screen.GAMEMENU
                    elif gameover and game_env.dynamic.active_screen != Screen.REPLAYMENU:                     # displaying the replay menu
                        active_sprite = ReplayText(game_env)
                        game_env.dynamic.active_screen = Screen.REPLAYMENU
                    game_env.dynamic.all_sprites.add(active_sprite)
                elif event.key == game_env.K_RETURN:                                                                # handling all [ENTER] key press activity
                    if game_env.dynamic.active_screen == Screen.GAMEMENU:                                      # selecting input mode in gamemenu screen
                        pygame.mouse.set_visible(True if game_env.dynamic.game_input == InputMode.MOUSE else False) # displaying mouse cursor based on user input mode
                        screen_color = game_env.static.background_default                                           # restoring screen colot
                        [sprite.kill() for sprite in title_sprites]                                                 # kill all the title_sprites sprite sprite
                        [game_env.dynamic.all_sprites.remove(sprite) for sprite in (active_sprite, hint_sprite)]
                        [game_env.dynamic.all_sprites.add(sprite) for sprite in (jet, scoretext_sprite)]            # adding the jet and scoreboard to all_sprites
                        [backgrounds.add(sprite) for sprite in vegetations.sprites()]
                        game_started = True                                                                         # starting game 
                    elif game_env.dynamic.active_screen == Screen.REPLAYMENU:                                       # selecting reply option in replaymenu screen
                        if game_env.dynamic.replay:
                            gameover = False                                                                        # setting gameover variable to false as user as opted to replay
                            jet = Jet(game_env)                                                                     # re-creating the jet
                            game_env.dynamic.ammo = 100
                            missiles.empty()                                                                        # empting the missle group                    
                            game_env.dynamic.all_sprites = pygame.sprite.Group()                                    # re-creating group of sprites 
                            [game_env.dynamic.all_sprites.add(sprite) for sprite in (jet, scoretext_sprite)]        # adding the jet and scoreboard to all_sprites
                            screen_color = game_env.static.background_default                                       # restoring  screen color
                            game_env.dynamic.game_playtime, game_env.dynamic.game_score, game_env.dynamic.game_level = 0, 0, 1 # resetting game data 
                            star_shown = False
                            pygame.time.set_timer(ADD_MISSILE, int(1000/game_env.static.missile_per_sec))
                            create_vegetation(game_env, vegetations)
                            [backgrounds.add(sprite) for sprite in vegetations.sprites()]
                        else:
                            running = False                                                         # stopping game as user as opted not to replay
                    
            if event.type == ADD_CLOUD:
                last_sprite = vegetations.sprites()[-1]                                             # storing the last available vegetation for computation
                if last_sprite.rect.x + last_sprite.rect.width/2 - game_env.static.screen_width < 0: # checking if the last vegetation has appeared in the screen, if yes a new vegetation will be created and appended
                    vegetation = Vegetation(game_env, x_pos=last_sprite.rect.x + last_sprite.rect.width+last_sprite.rect.width/2)   # position of the new sprite is after the last sprite
                    vegetations.add(vegetation)                                                     # adding sprite to groups for update and display
                    backgrounds.add(vegetation)

                new_cloud = Cloud(game_env)                                                         # is event to add cloud is triggered
                clouds.add(new_cloud)                                                               # create a new cloud
                backgrounds.add(new_cloud)                                                          # adding the cloud to all_sprites group
                if not gameover and game_started:
                    game_env.dynamic.game_playtime += 1                                             # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
                    if not star_shown and random.randint(0,30) % 3 == 0:                            # probabity of getting a star is 30%
                        star = Star(game_env)
                        stars.add(star)
                        game_env.dynamic.all_sprites.add(star)
                        star_shown = True
                    if game_env.dynamic.game_playtime % 20 == 0:                                    # changing game level very 20s
                        star_shown = False
                        game_env.dynamic.levelup_sound.play()                                       # playing level up sound
                        game_env.dynamic.game_level += 1                                            # increasing the game level
                        pygame.time.set_timer(ADD_MISSILE, int(1000/(game_env.static.missile_per_sec + int(game_env.dynamic.game_level/2)))) # updating timer of ADD_MISSLE for more missiles to be added
                        game_env.dynamic.ammo += 50                                                 # adding 50 ammo on each level up
                        game_env.dynamic.all_sprites.remove(game_env.dynamic.noammo_sprite)         # removing no ammo sprite when ammo is refilled
                        

        screen.fill(screen_color)                                                                   # Filling screen with sky blue color
        [screen.blit(sprite.surf, sprite.rect) for sprite in backgrounds]                           # drawing all backgrounds sprites
        [screen.blit(sprite.surf, sprite.rect) for sprite in game_env.dynamic.all_sprites]          # drawing all sprites in the screen

        

        # missile hit
        if pygame.sprite.spritecollideany(jet, missiles) and not gameover:                          # Check if any missiles have collided with the player; if so
            active_sprite = ReplayText(game_env)
            game_env.dynamic.active_screen = Screen.REPLAYMENU
            jet.kill()                                                                              # killing the jet
            game_env.dynamic.collision_sound.play()
            [game_env.dynamic.all_sprites.add(sprite) for sprite in (active_sprite, hint_sprite)]   # adding the gameover and the hint sprite
            game_env.dynamic.all_sprites.remove(game_env.dynamic.noammo_sprite)
            gameover = True                                                                         # setting gameover to true to prevent new missiles from spawning
            submit_result(game_env)
        
        # missile hit
        collision = pygame.sprite.groupcollide(missiles, game_env.dynamic.bullets, True, True)      # checking for collision between bullets and missiles, killing each one of them on collision
        if len(collision) > 0 and not gameover:
            game_env.dynamic.hit_sound.play()                                                       # play missile destroyed sound
            game_env.dynamic.game_score += len(collision) * 10                                      # 1 missle destroyed = 10 pts.

        # powerup hit
        if pygame.sprite.spritecollideany(jet, stars):                                              # collition between jet and star (powerup)
            game_env.dynamic.powerup_sound.play()
            [game_env.dynamic.all_sprites.remove(s) for s in stars.sprites()]                       # removing the star from all_sprites to hide from screen
            game_env.dynamic.game_score += 100 * game_env.dynamic.game_level                        # increasing game score by 100
            stars.empty()                                                                           # removing star from stars group
            for missile in missiles.sprites():                                                      
                missile.deactivate()                                                                # making missile as deactivated
                deactivated_missile.add(missile)                                                    # adding missile to deactivated_missile group
                missiles.remove(missile)                                                            # remove missiles from missles group to avoid collision with jet 
            
        pygame.display.flip()                                                                       # updating display to the screen
        gameclock.tick(game_env.static.fps)                                                         # ticking game clock at 30 to maintain 30fps

        pressed_keys = pygame.key.get_pressed()                                                     # getting all the pressed keys
        if game_started and not gameover and game_env.dynamic.game_input == InputMode.KEYBOARD:
            jet.update(pressed_keys)                                                                # calling update() to act according to pressed keys
        elif game_started and gameover:
            active_sprite.update(pressed_keys)                                                      # allowing user to select game replay option during gameover mode
        elif not game_started:
            active_sprite.update(pressed_keys)                                                      # allowing user to select game input type when the game is not started
            title_author_sprite.moveOnXaxis(2)                                                      # moving the game author sprite across the X axis   
        elif game_started and not gameover and game_env.dynamic.game_input == InputMode.MOUSE:      # performing the jet movement here for smooth movement till mouse cursor
            jet.auto_move(mouse_pos)

        if game_started:
            vegetations.update()                                                                    # vegetations will move only after the game starts

        game_env.dynamic.bullets.update()
        missiles.update()                                                                           # update the position of the missiles
        deactivated_missile.update()
        clouds.update()                                                                             # update the postition of the clouds
        stars.update()
        scoretext_sprite.update()                                                                   # update the game score

    pygame.mixer.music.stop()                                                                       # stopping game music
    pygame.mixer.quit()                                                                             # stopping game sound mixer


if __name__ == '__main__':  
    play()                                                                                          # starting game