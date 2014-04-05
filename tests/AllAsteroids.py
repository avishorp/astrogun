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

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=20, y=20,
                         background=(0.5, 0, 0, 1))
cam = pi3d.Camera()
shader = pi3d.Shader("uv_flat")

# Load all models 
zpos = 5
model_objs = []
dxy = 1.2
pos = (-dxy, -dxy)
global_scale = 0.6

for mf in models.asteroids:
  model_filename = mf[0]
  model_scale = mf[1]
  model_name = model_filename.split('.')[0] # Remove the .obj extention
  
  print("Loading " + model_name)
  
  m = pi3d.Model(file_string='../media/models/' + model_filename, 
                 name=model_name, 
                 x=pos[0], y=pos[1], z=zpos)
  m.set_shader(shader)
  m.scale(model_scale*global_scale, 
          model_scale*global_scale,
          model_scale*global_scale)
  model_objs.append(m)
  
  pos = (pos[0]+1, pos[1])
  if (pos[0] > dxy):
    pos = (-dxy, pos[1]+dxy)

# Fetch key presses
mykeys = pi3d.Keyboard()
t = time.time()
zpos = 50;
#mymodel.buf[0].set_textures(dino.buf[0].textures)

t = time.time()

while DISPLAY.loop_running():
  for m in model_objs:
    m.draw(camera=cam)
    
    m.rotateIncY(0.41)
    m.rotateIncZ(0.12)
    m.rotateIncX(0.23)

  #nt = time.time()
  #if (nt - t) > 1:
  #  model_objs[0].positionX(model_objs[0].x() + 0.2)
  #  t = nt
  
  k = mykeys.read()
  if k >-1:
    print(str(k))
    if k=='j':
      cam.rotateZ(0.5)
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
