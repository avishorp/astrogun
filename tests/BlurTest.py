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
                         background=(0, 0, 0, 1))
cam = pi3d.Camera()
shader = pi3d.Shader("uv_flat")
defocus = pi3d.Defocus()

# Load all models 
zpos = 5
model_objs = []
dxy = 1.2
global_scale = 0.6

mf=models.asteroids[5]
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
zpos = 50;
blur_amount = 10;

t = time.time()

while DISPLAY.loop_running():
  m=model_objs[0]
  defocus.start_blur()
  m.draw(camera=cam)
  defocus.end_blur()

  defocus.blur(m, -100, 100, blur_amount)
    
  m.rotateIncY(0.41)
  m.rotateIncZ(0.12)
  m.rotateIncX(0.23)

  #nt = time.time()
  #if (nt - t) > 1:
  #  model_objs[0].positionX(model_objs[0].x() + 0.2)
  #  t = nt
  
  k = mykeys.read()
  if k >-1:
    if k=='j':
      cam.rotateZ(0.5)
    elif k==ord('+'):
      m.translateZ(0.3)
    elif k==ord('-'):
      m.translateZ(-0.3)
    elif k==ord('q'):
      blur_amount -= 5
    elif k==ord('w'):
      blur_amount += 5
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
