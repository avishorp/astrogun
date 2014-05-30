from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.constants import *
from pi3d.Shape import Shape

class Cone(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None, radius=1.0, height=2.0, sides=12, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *radius*
        radius at bottom
      *height*
        height
      *sides*
        number of sides
    """
    super(Cone, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                               sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print("Creating Cone ...")

    path = []
    path.append((0.0, height * .5))
    path.append((0.0001, height * .5))
    path.append((radius, -height * .4999))
    path.append((radius, -height * .5))
    path.append((0.0001, -height * .5))
    path.append((0.0, -height * .5))

    self.radius = radius
    self.height = height
    self.ttype = GL_TRIANGLES

    self.buf = []
    self.buf.append(self._lathe(path, sides))
