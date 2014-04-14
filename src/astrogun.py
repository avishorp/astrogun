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
import util
import math

# Global Game Settings
######################

# Number of "lives" the player has initially
INITIAL_LIVES = 5

# The impact radius of the player (squared)
SELF_IMPACT_RADIUS2 = 5

# Impact raduis of an asteroid (squared)
ASTEROID_IMPACT_RADIUS = 10

# Bullet origin (the point from which the bullet starts)
BULLET_ORIGIN = numpy.array([0.0, -5.0, 0.0])

# The distance until which the bullet travels
BULLET_DISTANCE = 80

# The speed of a bullet
BULLET_SPEED = 2

###### END GLOBAL SETTINGS ######

class GameLevel:
  def __init__(self, asteroid_model_list, bullet_prototype):
    # Instantiate an Asteroid Generator
    self.gen = asteroids.AsteroidGenerator(asteroid_model_list, 1, None)
    self.active_asteroids = []
    self.active_bullets = []
    self.bullet_prototype = bullet_prototype
    self.direction = (0.0, 0.0) # azimuth, inclination, in degrees
    
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

      # Draw all active bullets
      objindex = 0
      for mobj, mmotion in self.active_bullets:
        newpos = mmotion.location(now)
        #  dist2_from_origin = newpos.dot(newpos)
        #  if dist2_from_origin < SELF_IMPACT_RADIUS2:
        #  # Reached origin, destory it
        #  del self.active_asteroids[objindex]
        #else:
        #  objindex += 1
      
        # Position, rotate and draw the asteroid
        mobj.position(newpos[0], newpos[1], newpos[2])
        mobj.draw()
  
      # TEMPORARY CODE
      k = keys.read()
      if k >-1:
        if k==260:
          # Left
          self.direction = (self.direction[0]-1, self.direction[1])
          cam.rotateY(1)
        elif k==261:
          # Right
          self.direction = (self.direction[0]+1, self.direction[1])
          cam.rotateY(-1)
        elif k==258:
          # Down
          self.direction = (self.direction[0], self.direction[1]-1)
          cam.rotateX(-1)
        elif k==259:
          # Up
          self.direction = (self.direction[0], self.direction[1]+1)
          cam.rotateX(1)
        elif k==ord(' '):
          eom = numpy.array([
              BULLET_DISTANCE*math.sin(math.radians(self.direction[0])), 
              BULLET_DISTANCE*math.sin(math.radians(self.direction[1])), 
              BULLET_DISTANCE])
          bullet_motion = util.LinearMotion(BULLET_ORIGIN, eom, BULLET_SPEED, now)
          p = self.bullet_prototype
          bullet_model = pi3d.Shape(cam, None, "ab", p.unif[0], p.unif[1], p.unif[2],
                                    p.unif[3], p.unif[4], p.unif[5], p.unif[6], p.unif[7],
                                    p.unif[8], p.unif[9], p.unif[10], p.unif[11])
          bullet_model.buf = p.buf
          bullet_model.shader = p.shader
          bullet_model.textures = p.textures
          self.active_bullets.append((bullet_model, bullet_motion))
        elif k==ord('1'):
          cam.rotateX(360.0)
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

bullet_prototype = pi3d.Sphere(radius=0.5)
bullet_prototype.set_shader(shader)

# Fetch key presses
mykeys = pi3d.Keyboard()
level = GameLevel(asteroid_model_list, bullet_prototype)
try:
  level.play(mykeys)
except:
  mykeys.close()
  DISPLAY.destroy()
  raise

mykeys.close()
DISPLAY.destroy()


