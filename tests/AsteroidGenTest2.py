#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Wavefront obj model loading. Material properties set in mtl file.
Uses the import pi3d method to load *everything*
"""

import sys
sys.path.append('../src')
import pi3d
import time
import models
import asteroids
import numpy

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=20, y=20,
                         background=(0, 0, 0, 1))
cam = pi3d.Camera()
shader = pi3d.Shader("uv_flat")
defocus = pi3d.Defocus()

# Load all models 
zpos = 5
model_objs = []
dxy = 1.2
global_scale = 0.6

model_list = []

for mf in models.asteroids[0:2]:
  model_filename = mf[0]
  model_scale = mf[1]
  model_name = model_filename.split('.')[0] # Remove the .obj extention
  
  print("Loading " + model_name)
  
  m = pi3d.Model(file_string='../media/models/' + model_filename, 
                 name=model_name, 
                 x=0, y=0, z=zpos)
  m.set_shader(shader)
  m.scale(model_scale*global_scale, 
        model_scale*global_scale,
        model_scale*global_scale)

  model_list.append(m)

# Instantiate an Asteroid Generator
  gen = asteroids.AsteroidGenerator(model_list, 1, None)
active_asteroids = []

# Fetch key presses
mykeys = pi3d.Keyboard()

t = time.time()
now = t

try:
  while DISPLAY.loop_running():
    now = time.time()
    ast = gen.generate_asteroid(now)
    if ast is not None:
      active_asteroids.append(ast)
    
    objindex = 0
    for mobj, mmotion in active_asteroids:
      newpos = mmotion.location(now)
      dist2_from_origin = newpos.dot(newpos)
      if dist2_from_origin < 5.0:
        # Reached origin, destory it
        del active_asteroids[objindex]
      else:
        objindex += 1
      
      mobj.position(newpos[0], newpos[1], newpos[2])
      mobj.draw()

    k = mykeys.read()
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
        mykeys.close()
        DISPLAY.destroy()
        break
except:
  mykeys.close()
  DISPLAY.destroy()
  raise
