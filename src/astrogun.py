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
  def __init__(self, sprites):
    # Instantiate an Asteroid Generator
    self.gen = asteroids.AsteroidGenerator(1, None)
    self.bullet_gen = bullets.BulletGenerator()
    self.active_asteroids = {}
    self.asteroid_id = 0
    self.active_bullets = []
    self.hit_asteroids = []
    self.azimuth = 0.0
    self.incl = 0.0
    self.self_hit = -1
    self.sprites = sprites
    self.fixed_sprites = []
    
    # Initial sprite location
    s = self.sprites['sight']
    s.position(*SIGHT_POSITION)
    s.scale(*SIGHT_SCALE)
    self.fixed_sprites.append(s)

    s = sprites['radar_panel']
    s.position(*RADAR_PANEL_POSITION)
    s.scale(*RADAR_PANEL_SCALE)
    self.fixed_sprites.append(s)

    s = sprites['radar_target']
    s.position(*TARGET_CENTER_POSITION)
    s.scale(*TARGET_SCALE)
    self.fixed_sprites.append(s)
    
  def create_bullet(self, now):
    b = self.bullet_gen.generate(self.azimuth, self.incl, now)
    self.active_bullets.append(b)
    
    # For all asteroids, check if the bullet hits them
    I = b.get_direction()
    indx = 0
    dest = None
    
    # Scan all the asteroids against incidence with the newly
    # created bullet. If more than one asteroid incides with
    # the bullet trajectory, pick the closest one
    for astid, ast in self.active_asteroids.items():
      if (self.check_incidence(ast, I)):
        if dest is None:
          dest = (astid, ast)
        else:
          if (ast.distance2() < dest[1].distance2()):
            dest = (astid, ast)
        
    b.set_destination(dest)

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

      # Self hit effect
      if self.self_hit > 0:
        DISPLAY.set_background(1.0, 0, 0, self.self_hit*1.0/10.0)
        if self.self_hit < 10:
          self.self_hit += 1
        else:
          self.self_hit = -1
          DISPLAY.set_background(1.0,0,0,0.0)
          
      # (possibly) generate a new asteroid
      ast = self.gen.generate_asteroid(now)
      if ast is not None:
        self.active_asteroids[self.asteroid_id] = ast
        self.asteroid_id += 1
    
      # Draw all active asteroid
      for astid, ast in self.active_asteroids.items():
        ast.move(now)
        dist2_from_origin = ast.distance2()

        if ast.hit_mode:
          if ast.hit_time > 8.0:
            del self.active_asteroids[astid]
        if dist2_from_origin < SELF_IMPACT_RADIUS2:
          # Reached origin, destory it
          del self.active_asteroids[astid]
          self.self_hit = 1
      
        # Position, rotate and draw the asteroid
        ast.draw()

      # Draw all hit asteroids
      for ast in self.hit_asteroids:
        ast.move(now)
        if ast.hit_time > 8.0:
          self.hit_asteroids[0]
          
        ast.draw()

      # Draw all active bullets
      objindex = 0
      for bull in self.active_bullets:
        bull.move(now)
        dest = bull.get_destination()
        dist2_from_origin = bull.distance2()
        
        if (dest is not None) and (dest[0] in self.active_asteroids):
          ast_distance2 = dest[1].distance2()
          if dist2_from_origin > ast_distance2:
            # Bullet hit the asteroid

            del self.active_asteroids[dest[0]]
            dest[1].hit(now)
            self.hit_asteroids.append(dest[1])
            del self.active_bullets[objindex]
        elif dist2_from_origin > BULLET_DISTANCE2:
          # Reached final distance, destroy it
          del self.active_bullets[objindex]
        else:
          objindex += 1
      
        bull.draw()

      # Draw Sprites
      for s in self.fixed_sprites:
        s.draw()
  
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


def load_sprites():
  sprite_filenames = ['sight', 'radar_panel', 'radar_target']
  sprites = {}
  sh = pi3d.Shader('uv_flat')
  
  for fn in sprite_filenames:
    s = pi3d.ImageSprite('../media/bitmaps/' + fn + '.png', shader = sh, w = 1, h = 1)
    sprites[fn] = s
    
  return sprites


# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(background=(1.0, 0, 0, 0))
cam = pi3d.Camera(at=[0.0, 0.0, 200.0], eye=[0.0, 0.0, 0.0])

SPRITES = load_sprites()

# Fetch key presses
mykeys = pi3d.Keyboard()
try:
  level = GameLevel(SPRITES)
  level.play(mykeys)
except:
  mykeys.close()
  DISPLAY.destroy()
  raise

mykeys.close()
DISPLAY.destroy()


