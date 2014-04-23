# Global Game Settings

from math import pi
import numpy

# Asteroid generation parametrs
###############################
SPEED_RANGE = (0.2, 0.4)
PHI_RANGE = (0, pi)
THETA_RANGE = (10.0/180.0*pi,170/180.0*pi)
INITIAL_DISTANCE = 50

PHI_RANGE = (0, 0.5)
THERA_RANGE = (0.5,0.8)

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
TARGET_SCALE = (0.3, 0.3, 1)
