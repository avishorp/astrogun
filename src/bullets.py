
import numpy, numpy.linalg, pi3d
from util import LinearMotion
from settings import *
import util

class Bullet:
    def __init__(self, prototype, azimuth, incl, speed, origin, distance, now):
        self.azimuth = azimuth
        self.incl = incl
        self.speed = speed
        eom = numpy.array(util.spher_to_cart(
                azimuth, 
                incl,
                distance
                )).clip(1e-3)
        self.motion = util.LinearMotion(origin, eom, speed, now)
        p = prototype
        self.bullet_model = pi3d.Shape(None, None, "bullet", p.unif[0], p.unif[1], p.unif[2],
                                  p.unif[3], p.unif[4], p.unif[5], p.unif[6], p.unif[7],
                                  p.unif[8], p.unif[9], p.unif[10], p.unif[11])
        self.bullet_model.buf = p.buf
        self.bullet_model.shader = p.shader
        self.bullet_model.textures = p.textures
        self.pos = origin
        self.direction = eom/numpy.linalg.norm(eom)

    def draw(self):
        self.bullet_model.draw()
        
    def move(self, t):
        self.pos = self.motion.location(t)
        self.bullet_model.position(self.pos[0], self.pos[1], self.pos[2])
        
    def distance2(self):
        return self.pos.dot(self.pos)
    
    def get_position(self):
        return self.pos
    
    def get_direction(self):
        return self.direction


class BulletGenerator:
    def __init__(self, shader):
        self.bullet_prototype = pi3d.Sphere(radius=0.5)
        self.bullet_prototype.set_shader(shader)
        
    def generate(self, azimuth, incl, now):
        b = Bullet(self.bullet_prototype, azimuth, incl, 
                   BULLET_SPEED, BULLET_ORIGIN, BULLET_DISTANCE,
                   now)
        return b
