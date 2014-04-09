import sys
sys.path.append('../src')

import asteroids
import time

TEST_TIME = 20

class ModelStub:
    def __init__(self, n):
        self.n = n
        self.x = None
        self.y = None
        self.z = None
        
    def clone(self):
        return ModelStub(self.n)
    
    def position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return "<Model %d (%f,%f,%f)>" % (self.n, self.x, self.y, self.z)

model_list = [
    ModelStub(1),
    ModelStub(2),
    ModelStub(3),
    ModelStub(4),
    ModelStub(5)
    ]

gen = asteroids.AsteroidGenerator(model_list, 2.0, None)
now = time.time()
t0 = now
total_generated = 0
while((now-t0) < TEST_TIME):
    g = gen.generate_asteroid(now)
    if g is not None:
        print("%d: Asteroid generated %s" % (now, str(g[0])))
        total_generated += 1
        
    now = time.time()

print("Total asteroids generated: %d" % total_generated)

