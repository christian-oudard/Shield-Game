"""A set of simple vector utility functions.

All functions take constant arguments, and return a result; nothing
is modified in-place.
"""

from __future__ import division
from math import sqrt, acos

def add(*args):
    """Calculate the vector addition of two or more vectors."""
    v_sum = args[0]
    for v in args[1:]:
        v_sum = _add(v_sum, v)
    return v_sum

def _add(v1, v2):
    return tuple((n1 + n2) for n1, n2 in zip(v1, v2))

def vecfrom(p1, p2):
    """Return the vector from p1 to p2."""
    return tuple((n2 - n1) for n1, n2 in zip(p1, p2))

def dot(v1, v2):
    """Calculate the dot product of two vectors."""
    return sum((n1 * n2) for n1, n2 in zip(v1, v2))

def cross(v1, v2):
    """Calculate the cross product of two vectors of size 3."""
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return (y1*z2 - z1*y2,
            z1*x2 - x1*z2,
            x1*y2 - y1*x2)

def mul(v, c):
    """Multiply a vector by a scalar."""
    return tuple(n*c for n in v)

def div(v, c):
    """Divide a vector by a scalar."""
    return tuple(n/c for n in v)

def neg(v):
    """Invert a vector."""
    return tuple(-n for n in v)

def mag2(v):
    """Calculate the squared magnitude of a vector."""
    return sum(n**2 for n in v)

def mag(v):
    """Calculate the magnitude of a vector."""
    return sqrt(mag2(v))

def dist2(p1, p2):
    """Find the squared distance between two points."""
    return mag2(vecfrom(p1, p2))

def dist(p1, p2):
    """Find the distance between two points."""
    return mag(vecfrom(p1, p2))

def norm(v, c=1):
    """Return a vector in the same direction as v, with magnitude c."""
    return mul(v, c/mag(v))

def avg(*args):
    """Find the vector average of two or more points."""
    return div(add(*args), len(args));

def angle(v1, v2):
    """Find the angle in radians between two vectors."""
    return acos(dot(v1, v2) / (mag(v1) * mag(v2)))
