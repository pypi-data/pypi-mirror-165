from math import cos
from VectorUtils.vector2 import Vector2
from VectorUtils.vector3 import Vector3


def dot(a: Vector2 | Vector3, b: Vector2 | Vector3, rad: float=0):
    '''
    Calculate Dot (Scaler) product of 2 vectors
    '''

    if (isinstance(a, (Vector2, Vector3))) and (isinstance(b, (Vector2, Vector3))):
        return a.magnitude() * b.magnitude() * cos(rad)
    else:
        raise Exception('invalid type for dot product, not a vector')
