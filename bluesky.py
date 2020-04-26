# Import the pygame module
import pygame
from game.data import InputMode
from game.environment import GameEnvironment
from game.sprites.jet import Jet
from game.sprites.missile import Missile
from game.sprites.cloud import Cloud
from game.sprites.text import Text
from game.sprites.text.score import ScoreText
from game.sprites.text.replay import ReplayText
from game.sprites.text.gameinput import GameInputText

__version__ = 0.6               # setting game version
__name__ = 'Bluesky'            # setting game name    

def show_gameover(game_env, replaytext_sprite):
    gameover_txt = Text(game_env, "GAME OVER", 60, x_pos=game_env.constants.screen_width/2 - 10 ,y_pos = game_env.constants.screen_height/2-25)        # creating game over message sprite
    game_env.variables.all_sprites.add(gameover_txt)                # adding gameover text sprite to all_sprites for repetated rendereing incase of gameover
    game_env.variables.all_sprites.add(replaytext_sprite)           # adding replay text sprite to all_sprites for repetated rendereing incase of gameover


def play_bluesky():
    pygame.mixer.init()                                                 # initializing same audio mixer with default settings
    pygame.init()                                                       # initializing pygame
    game_env = GameEnvironment()                                        # initializing game environment

    game_env.variables.moveup_sound.set_volume(0.5)
    game_env.variables.movedown_sound.set_volume(0.5)
    game_env.variables.collision_sound.set_volume(1)

    pygame.mixer.music.load(game_env.constants.game_sound.get('music'))     # setting main game background music
    pygame.mixer.music.play(loops=-1)                                       # lopping the main game music

    screen = pygame.display.set_mode((game_env.constants.screen_width, game_env.constants.screen_height))     # creating game screen with custom width and height
    pygame.display.set_caption('{} ver. {}'.format(__name__, __version__))              # setting name of game window
    pygame.mouse.set_visible(False)                                                     # hiding the mouse pointer from the game screen

    gameclock = pygame.time.Clock()                                                     # setting up game clock to maintain constant fps

    ADD_MISSILE = pygame.USEREVENT + 1                                                  # creating custom event to automatically add missiles in the screen
    pygame.time.set_timer(ADD_MISSILE, int(1000/game_env.constants.missile_per_sec))    # setting event to auto-trigger every 500ms; 2 missiles will be created every second

    ADD_CLOUD = pygame.USEREVENT + 2                                                    # creating custom event to automatically add cloud in the screen
    pygame.time.set_timer(ADD_CLOUD, int(1000/game_env.constants.cloud_per_sec))        # setting event to auto-trigger every 1s; 1 cloud will be created every second

    running = True                                                                      # game running variable
    gameover = False                                                                    # no gameover by default
    game_started = False                                                                # game is not started by default
    game_score = 0                                                                      # default game score
    game_playtime = 0                                                                   # default game playtime
    mouse_pos = (game_env.constants.screen_width, game_env.constants.screen_height/2)   # default mouse position, let the jet move forward on a straight line
    screen_color = game_env.constants.background_default if game_started else game_env.constants.background_special

    gameinput_sprite = GameInputText(game_env)                                          # creating GameInputText sprite
    game_env.variables.all_sprites.add(gameinput_sprite)                                # adding GameInputText to all_sprites group to be drawn on the screen

    clouds = pygame.sprite.Group()                                                      # creating cloud group for storing all the clouds in the game
    missiles = pygame.sprite.Group()                                                    # creating missile group for storing all teh missiles in the game

    jet = Jet(game_env)                                                                 # creating jet sprite
    scoretext_sprite = ScoreText(game_env)                                              # creating scoreboard sprite
    replaytext_sprite = ReplayText(game_env)                                            # creating ReplayText sprite

    # Main game loop
    while running:
        for event in pygame.event.get():                                                                                        # Look at every event in the queue
            if event.type == game_env.KEYDOWN and event.key == game_env.K_ESCAPE or event.type == game_env.QUIT:                # stopping game when ESC key is pressed or when the game window is closed
                running = False
            elif not gameover and game_env.variables.game_input ==  InputMode.MOUSE and event.type == game_env.MOUSEMOTION:     # moving jet based on mouse movement
                mouse_pos = pygame.mouse.get_pos()                                                                              # saving the mouse co-ordinate for smooth movement later
            elif not game_started and event.type == game_env.KEYDOWN and event.key == game_env.K_RETURN:                        # checking game input mode
                pygame.mouse.set_visible(True if game_env.variables.game_input == InputMode.MOUSE else False)                   # displaying mouse cursor based on user input mode
                screen_color = game_env.constants.background_default                                                            # restoring screen colot
                game_started = True                                                                                             # starting game               
                gameinput_sprite.kill()                                                                                         # killing the GameInputText sprite
                game_env.variables.all_sprites.add(jet)                                                                         # adding the jet to all_sprites
                game_env.variables.all_sprites.add(scoretext_sprite)                                                     # adding the scoreboard to all_sprites
            elif gameover and event.type == game_env.KEYDOWN and event.key == game_env.K_RETURN and game_started: # checking for replay text only after the game is started
                if replaytext_sprite.replay_choice:
                    gameover = False                                            # setting gameover variable to false as user as opted to replay
                    jet = Jet(game_env)                                         # re-creating the jet
                    game_env.variables.all_sprites = pygame.sprite.Group()      # re-creating group of sprites 
                    game_env.variables.all_sprites.add(jet)                     # adding the jet to all_sprites
                    game_env.variables.all_sprites.add(scoretext_sprite)        # adding the scoreboard to all_sprites
                    clouds.empty()                                              # empting the cloud group
                    missiles.empty()                                            # empting the missle group
                    screen_color = game_env.constants.background_default        # restoring  screen color
                    game_score, game_playtime = 0, 0                            # reseting game score and playtime
                else:
                    running = False                                             # stopping game as user as opted not to replay
            elif not gameover and game_started and event.type == ADD_MISSILE:   # is event to add missile is triggered; missles are not added during gameover
                new_missile = Missile(game_env)                                 # create a new missile
                missiles.add(new_missile)                                       # adding the missile to missle group
                game_env.variables.all_sprites.add(new_missile)                 # adding the missile to all_sprites group as well
            elif event.type == ADD_CLOUD:
                new_cloud = Cloud(game_env)                                     # is event to add cloud is triggered
                clouds.add(new_cloud)                                           # create a new cloud
                game_env.variables.all_sprites.add(new_cloud)                   # adding the cloud to all_sprites group
                if not gameover and game_started:
                    game_playtime += 1                                          # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
                    game_score += 10                                            # increasing score by 10 as this event is triggered every second

        screen.fill(screen_color)                                               # Filling screen with sky blue color
        [screen.blit(sprite.surf, sprite.rect) for sprite in game_env.variables.all_sprites]    # drawing all sprites in the screen

        if pygame.sprite.spritecollideany(jet, missiles):                       # Check if any missiles have collided with the player; if so
            jet.kill()                                                          # killing the jet
            game_env.variables.moveup_sound.stop()
            game_env.variables.movedown_sound.stop()
            game_env.variables.collision_sound.play()
            show_gameover(game_env, replaytext_sprite)                          # showing gameover sprite
            gameover = True                                                     # setting gameover to true to prevent new missiles from spawning

        pygame.display.flip()                                                   # updating display to the screen
        gameclock.tick(game_env.constants.fps)                                                     # ticking game clock at 30 to maintain 30fps

        pressed_keys = pygame.key.get_pressed()                                 # getting all the pressed keys
        if game_started and not gameover and game_env.variables.game_input == InputMode.KEYBOARD:
            jet.update(pressed_keys)                                            # calling update() to act according to pressed keys
        elif game_started and gameover:
            replaytext_sprite.update(pressed_keys)                              # allowing user to select game replay option during gameover mode
        elif not game_started:
            gameinput_sprite.update(pressed_keys)                               # allowing user to select game input type when the game is not started
        elif game_started and not gameover and game_env.variables.game_input == InputMode.MOUSE:     # performing the jet movement here for smooth movement till mouse cursor
            jet.auto_move(mouse_pos)

        missiles.update()                                                       # update the position of the missiles
        clouds.update()                                                         # update the postition of the clouds
        scoretext_sprite.update(game_playtime, game_score)                      # update the game score

    pygame.mixer.music.stop()                                                   # stopping game music
    pygame.mixer.quit()                                                         # stopping game sound mixer


if __name__ == 'Bluesky':  
    play_bluesky()                                                              # starting game