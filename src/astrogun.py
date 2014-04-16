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

from settings import *


class GameLevel:
  def __init__(self, asteroid_model_list, bullet_prototype):
    # Instantiate an Asteroid Generator
    self.gen = asteroids.AsteroidGenerator(asteroid_model_list, 1, None)
    self.active_asteroids = []
    self.active_bullets = []
    self.bullet_prototype = bullet_prototype
    self.azimuth = 0.0
    self.incl = 0.0
    
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
      for mobj, mmotion in self.active_bullets:
        newpos = mmotion.location(now)
        dist2_from_origin = newpos.dot(newpos)
        if dist2_from_origin > BULLET_DISTANCE2:
          # Reached final distance, destroy it
          del self.active_bullets[objindex]
        else:
          objindex += 1
      
        # Position, rotate and draw the asteroid
        mobj.position(newpos[0], newpos[1], newpos[2])
        mobj.draw()
  
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
          eom = numpy.array(util.spher_to_cart(
                self.azimuth, 
                self.incl,
                BULLET_DISTANCE
                )).clip(1e-1)
          print("%f %f" %(self.azimuth, self.incl))
          print(eom)
          bullet_motion = util.LinearMotion(BULLET_ORIGIN, eom, BULLET_SPEED, now)
          p = self.bullet_prototype
          bullet_model = pi3d.Shape(cam, None, "ab", p.unif[0], p.unif[1], p.unif[2],
                                    p.unif[3], p.unif[4], p.unif[5], p.unif[6], p.unif[7],
                                    p.unif[8], p.unif[9], p.unif[10], p.unif[11])
          bullet_model.buf = p.buf
          bullet_model.shader = p.shader
          bullet_model.textures = p.textures
          self.active_bullets.append((bullet_model, bullet_motion))
          
          #cam.reset()
          #tilt, rot = cam.point_at(eom)
          #print("rot=%f azimuth=%f\n" % (rot, self.azimuth))
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


