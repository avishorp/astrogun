#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Wavefront obj model loading. Material properties set in mtl file.
Uses the import pi3d method to load *everything*
"""

import sys
sys.path.append('../src')
import pi3d
import time
from asteroids import models

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=20, y=20,
                         background=(0, 0, 0, 1))
cam = pi3d.Camera()
shader = pi3d.Shader("uv_flat_explode")

# Load all models 
zpos = 7
model_objs = []
dxy = 1.2
global_scale = 0.6

mf=models[5]
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
model_objs.append(m)

# Fetch key presses
mykeys = pi3d.Keyboard()
t = time.time()
tx = 1.0
while DISPLAY.loop_running():
  m=model_objs[0]
  m.set_custom_data(21, (tx,tx,tx))
  m.draw(camera=cam)

  tx += 0.1

  k = mykeys.read()
  if k >-1:
    if k=='j':
      cam.rotateZ(0.5)
    elif k==ord('+'):
      m.translateZ(2.0)
    elif k==ord('-'):
      m.translateZ(-2.0)
    elif k==ord('q'):
      blur_amount -= 5
    elif k==ord('w'):
      blur_amount += 5
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
