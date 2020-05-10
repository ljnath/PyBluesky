from pygame import display

class StaticData():
    """ Class which holds all the static game values
    """
    def __init__(self):
        self.__display_info = display.Info()                        # get current display information

    @property
    def name(self):
        return 'PyBluesky'

    @property
    def version(self):
        return '1.0.2'

    @property
    def screen_width(self):
        return self.__display_info.current_w                        # game resolution is same as monitor resolution
        # return 1024

    @property
    def screen_height(self):
        return self.__display_info.current_h                        # game resolution is same as monitor resolution
        # return 768
    
    @property
    def text_default_color(sef):
        return (255,0,0)                    # default color is red
    
    @property
    def text_selection_color(sef):
        return (0,0,255)                    # selection color is blue

    @property
    def game_icon(self):
        return 'icon/pybluesky.ico'                  # jet image path

    @property
    def game_font(self):
        return 'font/arcade.ttf'            # game font file path

    @property
    def clouds(self):
        return ('image/cloud1.png', 'image/cloud2.png', 'image/cloud3.png') # all game cloud designs

    @property
    def vegetation(self):
        return ('image/vegetation_plain.png', 'image/vegetation_tree.png')

    @property
    def ground(self):
        return 'image/ground.png'

    @property
    def grass(self):
        return 'image/grass.png'

    @property
    def sam_launcher(self):
        return 'image/samlauncher.png'

    @property
    def sam(self):
        return 'image/sam.png'

    @property
    def missile_activated_image(self):
        return 'image/missile_activated.png'    # missle image path

    @property
    def missile_deactivated_image(self):
        return 'image/missile_deactivated.png'  # missle image path

    @property
    def jet_image(self):
        return 'image/jet.png'                  # jet image path

    @property
    def powerup_image(self):
        return 'image/star.png'                 # jet image path

    @property
    def bullet_image(self):
        return 'image/bullet.png'               # bullet image path

    @property
    def cloud_per_sec(self):
        return 1                            # number of cloud to be spawned per second

    @property
    def missile_per_sec(self):
        return 2                            # number of missiles to be spawned per seconds

    @property
    def background_default(self):
        return (208, 244, 247)              # skyblue color

    @property
    def background_special(self):
        return (196, 226, 255)              # pale skyblue

    @property
    def fps(self):
        return 30                           # game should run at 30 pfs

    @property
    def max_ammo(self):
        return 999

    @property
    def player_file(self):
        return 'data/player.dat'

    @property
    def name_length(self):
        return 12
        
    @property
    def game_sound(self):
        return {
            'music' : 'audio/music.ogg',
            'collision' : 'audio/collision.ogg',
            'levelup' : 'audio/levelup.ogg',
            'shoot' : 'audio/shoot.ogg',
            'hit' : 'audio/missile_hit.ogg',
            'powerup' : 'audio/powerup.ogg',
            'samfire' : 'audio/fire.ogg'
        }

