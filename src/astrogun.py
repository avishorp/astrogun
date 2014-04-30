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
    self.gen = asteroids.AsteroidGenerator(0.1, None)
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
    self.lives = INITIAL_LIVES
    self.scores = 0
    self.scores_changed = True
    self.frames = 0
    
    # Initial sprite location
    s = self.sprites['sight']
    s.position(*SIGHT_POSITION)
    s.scale(*SIGHT_SCALE)
    self.fixed_sprites.append(s)

    s = sprites['radar_panel']
    s.position(*RADAR_PANEL_POSITION)
    s.scale(*RADAR_PANEL_SCALE)
    self.fixed_sprites.append(s)
    
    self.radar_target = sprites['radar_target']
    self.radar_target.scale(*TARGET_SCALE)
    
    self.life_full = sprites['life_full']
    self.life_full.scale(*LIFE_BAR_SCALE)

    self.life_empty = sprites['life_empty']
    self.life_empty.scale(*LIFE_BAR_SCALE)

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
    start_time = now
    
    while DISPLAY.loop_running():
      now = time.time()
      self.frames += 1
      
      # Self hit effect
      if self.self_hit > 0:
        DISPLAY.set_background(self.self_hit*1.0/10.0, 0, 0, 1)
        if self.self_hit < 10:
          self.self_hit += 1
        else:
          self.self_hit = -1
          DISPLAY.set_background(0.0,0,0,1.0)
          
      # (possibly) generate a new asteroid
      ast = self.gen.generate_asteroid(now)
      if ast is not None:
        self.active_asteroids[self.asteroid_id] = ast
        self.asteroid_id += 1
    
      # Draw all active asteroid
      for astid, ast in self.active_asteroids.items():
        # Draw the asteroid itseld
        ast.move(now)
        dist2_from_origin = ast.distance2()
        
        # Draw the target on the radar view
        dist_from_origin = (math.sqrt(dist2_from_origin)/INITIAL_DISTANCE)*TARGET_DIST_SCALE
        angle = math.radians(ast.azimuth + self.azimuth + 90)
        rtx = dist_from_origin*math.cos(angle)
        rty = dist_from_origin*math.sin(angle)
        self.radar_target.position(TARGET_CENTER_POSITION[0]+rtx, 
                                   TARGET_CENTER_POSITION[1]+rty,
                                   TARGET_CENTER_POSITION[2])
        self.radar_target.draw(camera = cam2d)

        if ast.hit_mode:
          if ast.hit_time > 8.0:
            del self.active_asteroids[astid]
        if dist2_from_origin < SELF_IMPACT_RADIUS2:
          # Reached origin, destory it
          del self.active_asteroids[astid]
          self.self_hit = 1
          self.lives -= 1
      
        # Position, rotate and draw the asteroid
        ast.draw(camera = cam3d)

      # Draw all hit asteroids
      for ast in self.hit_asteroids:
        ast.move(now)
        if ast.hit_time > 8.0:
          self.hit_asteroids[0]
          
        ast.draw(camera = cam3d)

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
      
        bull.draw(camera = cam3d)

      # Draw Sprites
      for s in self.fixed_sprites:
        s.draw(camera = cam2d)
        
      # Draw lives
      for l in range(0, 5):
        if l+1 > self.lives:
          s = self.life_empty
        else:
          s = self.life_full
        s.position(LIFE_BAR_POSITION[0],
                   LIFE_BAR_POSITION[1] + l*LIFE_BAR_STEP,
                   LIFE_BAR_POSITION[2])
        s.draw(camera = cam2d)

      # Draw scores
      if self.scores_changed:
        self.scores_str = pi3d.String(font=computer_font, 
                                      string="%03d" % self.scores,
                                      x = SCORE_POSITION[0],
                                      y = SCORE_POSITION[1],
                                      z = SCORE_POSITION[2],
                                      sx=0.01, sy=0.01)
        self.scores_str.set_shader(shader_uv_flat)
        scores_changed = False

      self.scores_str.draw(camera = cam2d)

      # Debugging
      #debug_str = "az: %f incl: %f" % (self.azimuth, self.incl)
      #debug_str_pi = pi3d.String(font=arial_font, string=debug_str,
      #                           x = 0, y = 0, z = 5, sx=0.005, sy=0.005)
      #debug_str_pi.set_shader(shader_uv_flat)
      #debug_str_pi.draw(camera = cam2d)
  
      # TEMPORARY CODE
      k = keys.read()
      cam_rotate = False
      if k >-1:
        if k==260:
          # Left
          self.azimuth -= 1.0
          #cam3d.rotateY(1.0)
          cam_rotate = True
        elif k==261:
          # Right
          self.azimuth += 1.0
          #cam3d.rotateY(-1.0)
          cam_rotate = True
        elif k==258:
          # Down
          #cam3d.rotateX(-1)
          self.incl -= 1.0
          cam_rotate = True
        elif k==259:
          # Up
          #cam3d.rotateX(1)
          self.incl += 1.0
          cam_rotate = True
        elif k==ord(' '):
          self.create_bullet(now)
        elif (k == 27):
          break
      
      # Handle camera rotation
      if cam_rotate:
        cam3d.reset()
        cam3d.rotateX(self.incl)
        cam3d.rotateY(-self.azimuth)

      # If no more lives left, terminate the game
      if self.lives == 0:
        break
      
    # Calculate average FPS
    end_time = time.time()
    self.FPS = (1.0*self.frames)/(1.0*(end_time - start_time))

def load_sprites():
  sprite_filenames = ['sight', 'radar_panel', 'radar_target', 'life_full', 'life_empty', 'trans']
  sprites = {}
  sh = shader_uv_flat
  
  for fn in sprite_filenames:
    s = pi3d.ImageSprite('../media/bitmaps/' + fn + '.png', shader = sh, w = 1, h = 1)
    sprites[fn] = s
    
  return sprites


# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(background=(0.0, 0, 0, 1))
DISPLAY.frames_per_second = 30

ASPECT = DISPLAY.width / DISPLAY.height
cam3d = pi3d.Camera((0,0,0), (0,0,-0.1), (1, 1000, 45, ASPECT), is_3d=True)
cam2d = pi3d.Camera(is_3d=True)
shader_uv_flat = pi3d.Shader('uv_flat')
shader_mat_flat = pi3d.Shader('mat_flat')
arial_font = pi3d.Font("fonts/FreeMonoBoldOblique.ttf", (221,0,170,255))
computer_font = pi3d.Font("../media/fonts/Computerfont.ttf", (0,0,255,255))

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

print("lives: %d\n" % level.lives)
print("FPS: %f\n" % level.FPS)
