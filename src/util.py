import math, numpy

# Holds a point in 3D polar (spherical) coordinates
class PolarCoord:
    def __init__(self, r, phi, tetha):
        self.r = r
        self.phi = phi
        self.tetha = tetha
        
    def to_cartesian(self):
        x = self.r * math.sin(self.tetha)*math.cos(self.phi)
        y = self.r * math.sin(self.tetha)*math.sin(self.phi)
        z = self.r * math.cos(self.tetha)
        return (x, y, z)

# Covert from spherical coordinates
# into cartesian (adjusted for pi3d coordinate system, where
# X-Y plane is the screen)
# See reference: http://www.geom.uiuc.edu/docs/reference/CRC-formulas/node42.html
#
# az - Azimuth (in degrees)
# incl - Inclination (in degreez)
def spher_to_cart(az, incl, r):
    phi = math.radians(90 - incl)
    theta = math.radians(az)
    
    x = r * math.cos(theta)*math.sin(phi)
    y = r * math.sin(theta)*math.sin(phi)
    z = r * math.cos(phi)

    return (y, z, x)


class LinearMotion:
    # from_location - Initial object location
    # to_location - Final object location
    # speed - The speed of the item towards the origin
    # t0 - The initial time
    def __init__(self, from_location, to_location, speed, t0):
        self.b = from_location
        self.t0 = t0
        self.a = (to_location-from_location)*speed

    def location(self, t):
        dt = t - self.t0
        return self.b + self.a*dt

