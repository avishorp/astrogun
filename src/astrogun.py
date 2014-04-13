#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Wavefront obj model loading. Material properties set in mtl file.
Uses the import pi3d method to load *everything*
"""

import sys
sys.path.append('../src')
import pi3d
import time
import asteroids
import numpy

# Global Game Settings
######################

# Number of "lives" the player has initially
INITIAL_LIVES = 5

# The impact radius of the player (squared)
SELF_IMPACT_RADIUS2 = 5

# Impact raduis of an asteroid (squared)
ASTEROID_IMPACT_RADIUS = 10

###### END GLOBAL SETTINGS ######

class GameLevel:
  def __init__(self, asteroid_model_list):
    # Instantiate an Asteroid Generator
    self.gen = asteroids.AsteroidGenerator(asteroid_model_list, 1, None)
    self.active_asteroids = []

  def play(self, keys):
    now = time.time()

    while DISPLAY.loop_running():
      now = time.time()
      
      # (possibly) generate a new asteroid
      ast = self.gen.generate_asteroid(now)
      if ast is not None:
        self.active_asteroids.append(ast)
    
      # Draw all active asteroid
      objindex = 0
      for mobj, mmotion in self.active_asteroids:
        newpos = mmotion.location(now)
        dist2_from_origin = newpos.dot(newpos)
        if dist2_from_origin < SELF_IMPACT_RADIUS2:
          # Reached origin, destory it
          del self.active_asteroids[objindex]
        else:
          objindex += 1
      
        # Position, rotate and draw the asteroid
        mobj.position(newpos[0], newpos[1], newpos[2])
        mobj.rotateIncX(0.2)
        mobj.rotateIncY(0.3)
        mobj.draw()
  
      # TEMPORARY CODE
      k = keys.read()
      if k >-1:
        if k==260:
          # Left
          cam.rotateY(0.5)
        elif k==261:
          # Right
          cam.rotateY(-0.5)
        elif k==258:
          # Down
          cam.rotateX(-.5)
        elif k==259:
          # Up
          cam.rotateX(-0.5)
        elif k==27:
          break



# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=20, y=20,
                         background=(0, 0, 0, 1))
cam = pi3d.Camera()
shader = pi3d.Shader("uv_flat")

# Load all asteroid models 
asteroid_model_list = []
global_scale = 1.0
for mf in asteroids.models[0:3]:
  model_filename = mf[0]
  model_scale = mf[1]
  model_name = model_filename.split('.')[0] # Remove the .obj extention
  
  print("Loading " + model_name)
  
  m = pi3d.Model(file_string='../media/models/' + model_filename, 
                 name=model_name)
  m.set_shader(shader)
  m.scale(model_scale*global_scale, 
        model_scale*global_scale,
        model_scale*global_scale)
  
  asteroid_model_list.append(m)

# Fetch key presses
mykeys = pi3d.Keyboard()
level = GameLevel(asteroid_model_list)
level.play(mykeys)
mykeys.close()
DISPLAY.destroy()

