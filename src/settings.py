# Global Game Settings

from math import pi, radians
import numpy

# Asteroid generation parametrs
###############################
SPEED_RANGE = (0.2, 0.4)
INCLINATION_RANGE = (10.0, 60.0)
AZIMUTH_RANGE = (-180.0, 180.0)
INITIAL_DISTANCE = 50.0

# Directories and Filenames
###########################
VAR_DIR = "./var"     # Working directory
AST_DB_FILENAME = "asteroids_db.bin"

#######################################

# Number of "lives" the player has initially
INITIAL_LIVES = 5

# The impact radius of the player (squared)
SELF_IMPACT_RADIUS2 = 5

# Impact raduis of an asteroid (squared)
ASTEROID_IMPACT_RADIUS = 6

# Bullet origin (the point from which the bullet starts)
BULLET_ORIGIN = numpy.array([0.0, -2.0, 0.0])

# The distance until which the bullet travels
BULLET_DISTANCE = 200.0
BULLET_DISTANCE2 = BULLET_DISTANCE*BULLET_DISTANCE

# The speed of a bullet
BULLET_SPEED = 2.0

#######################################
### SPRITE DETAILS

SIGHT_POSITION = (0, 0, 4.8)
SIGHT_SCALE = (1, 1, 1)

RADAR_PANEL_POSITION = (2, -1, 4.8)
RADAR_PANEL_SCALE = (1.3, 1.3, 1)

TARGET_CENTER_POSITION = (2-0.03, -1+0.02, 4.7)
TARGET_SCALE = (0.2, 0.2, 1)
TARGET_DIST_SCALE = 0.6

LIFE_BAR_SCALE = (0.28, 0.08, 1)
LIFE_BAR_POSITION = (-3.2, 1.3, 4.7) # The lowest bar
LIFE_BAR_STEP = 0.1

SCORE_POSITION = (-2.5, 1.45, 4.5)

# Initial number of lives
INITIAL_LIVES = 5

# Sounds
SHOOTING_SOUND = '../media/sounds/match3.wav'
EXPLODE_SOUND = ''
HIT_SOUND = ''

# I/O Buttons and Actuator Mappings
BUTTON_START_GPIO = 4
BUTTON_FIRE_GPIO = 17
RUMBLE_FIRE_GPIO = 22
