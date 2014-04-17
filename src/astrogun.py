#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Wavefront obj model loading. Material properties set in mtl file.
Uses the import pi3d method to load *everything*
"""

import sys
sys.path.append('../src')
import pi3d
import time
import asteroids, bullets
import numpy, numpy.linalg
import util
import math

from settings import *


class GameLevel:
  def __init__(self, asteroid_model_list, bullet_shader):
    # Instantiate an Asteroid Generator
    self.gen = asteroids.AsteroidGenerator(asteroid_model_list, 1, None)
    self.bullet_gen = bullets.BulletGenerator(bullet_shader)
    self.active_asteroids = []
    self.active_bullets = []
    self.azimuth = 0.0
    self.incl = 0.0

  def create_bullet(self, now):
    b = self.bullet_gen.generate(self.azimuth, self.incl, now)
    self.active_bullets.append(b)
    
    # For all asteroids, check if the bullet hits them
    I = b.get_direction()
    indx = 0
    for ast in self.active_asteroids:
      if (self.check_incidence(ast, I)):
        del self.active_asteroids[indx]
      else:
        indx += 1

  # Check wheter a bullet will hit an asteroid. 
  # asteroid - An Asteroid class object
  # bullet - A unit vector designating the bullet direction
  #
  # The test is based on a line-sphere intersection test, as described
  # in http://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
  # We are not interested in the full solution of the equation, only whether
  # the term under square root is non-negative. Also, the bullets always
  # originate at the origin (0,0,0) simplifying the equation further
  def check_incidence(self, asteroid, bullet):
    c = asteroid.get_position()
    r = asteroid.radius
    I = bullet
    
    sq = (I.dot(c))**2 - (I.dot(I)*(c.dot(c) - r**2))
    return (sq >= 0)

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
      for mobj in self.active_asteroids:
        mobj.move(now)
        dist2_from_origin = mobj.distance2()

        if dist2_from_origin < SELF_IMPACT_RADIUS2:
          # Reached origin, destory it
          del self.active_asteroids[objindex]
        else:
          objindex += 1
      
        # Position, rotate and draw the asteroid
        mobj.draw()

      # Draw all active bullets
      objindex = 0
      for bull in self.active_bullets:
        bull.move(now)
        dist2_from_origin = bull.distance2()
        if dist2_from_origin > BULLET_DISTANCE2:
          # Reached final distance, destroy it
          del self.active_bullets[objindex]
        else:
          objindex += 1
      
        bull.draw()
  
      # TEMPORARY CODE
      k = keys.read()
      if k >-1:
        if k==260:
          # Left
          self.azimuth -= 1.0
          cam.rotateY(1.0)
        elif k==261:
          # Right
          self.azimuth += 1.0
          cam.rotateY(-1.0)
        elif k==258:
          # Down
          cam.rotateX(-1)
          self.incl -= 1.0
        elif k==259:
          # Up
          cam.rotateX(1)
          self.incl += 1.0
        elif k==ord(' '):
          self.create_bullet(now)

        elif k==ord('1'):
          cam.rotateY(25.0)
          #self.azimuth = 25.0
        elif k==27:
          break



# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=20, y=20,
                         background=(0, 0, 0, 1))
cam = pi3d.Camera(at=[0.0, 0.0, 200.0], eye=[0.0, 0.0, 0.0])
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
try:
  level = GameLevel(asteroid_model_list, shader)
  level.play(mykeys)
except:
  mykeys.close()
  DISPLAY.destroy()
  raise

mykeys.close()
DISPLAY.destroy()


