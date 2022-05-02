"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
02.05.22 20:20

A class that represents a 2D vector for the simulation

Inspiration:
https://scipython.com/book2/chapter-4-the-core-python-language-ii/examples/a-2d-vector-class/
"""


import math

class Vector2D:
    # cartesian values
    _valx: float = 0
    _valy: float = 0

    def __init__(self, x: float, y: float):
        self._valx, self._valy = x, y

    # properties for cartesian values
    @property
    def x(self) -> float:
        return self._valx
    
    @x.setter
    def x(self, value):
        self._valx = value

    @property
    def y(self) -> float:
        return self._valy
    
    @y.setter
    def y(self, value):
        self._valy = value
    
    @property
    def cart(self) -> tuple[float, float]:
        return (self._valx, self._valy)
    
    @cart.setter
    def cart(self, value: tuple[float, float]):
        self._valx = value[0]
        self._valy = value[1]

    # properties for polar values
    @property
    def r(self) -> float:
        return math.sqrt(pow(self._valx, 2) + pow(self._valy, 2))
    
    @r.setter
    def r(self, value):
        keepphi = self.phi
        self._valx = math.cos(keepphi) * value
        self._valy = math.sin(keepphi) * value
    
    @property
    def phi(self) -> float:
        return math.atan2(self._valy, self._valx)
    
    @phi.setter
    def phi(self, value):
        keepr = self.r
        self._valx = math.cos(value) * keepr
        self._valy = math.sin(value) * keepr


    # operators
    
    def __str__(self):
        # Human-readable string representation of the vector
        return '({:g};{:g})'.format(self.x, self.y)

    def __repr__(self):
        # Unambiguous string representation of the vector
        return repr((self.x, self.y))

    def dot(self, other):
        # The scalar (dot) product of self and other. Both must be vectors
        if not isinstance(other, Vector2D):
            raise TypeError("Can only dot-multiply Vector2D by Vector2D")
        return self.x * other.x + self.y * other.y
    
    # Alias the __matmul__ method to enable matrix multiplication with "a @ b" syntax
    __matmul__ = dot

    def __sub__(self, other):
        # Vector subtraction
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        # Vector addition
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        # Multiplication of a vector by a scalar (single factor)

        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector2D(self.x*scalar, self.y*scalar)
        raise NotImplementedError('Can only multiply Vector2D by a number')

    def __rmul__(self, scalar):
        # Reflected multiplication so scalar * vector also works
        return self.__mul__(scalar)

    def __neg__(self):
        # Negation of the vector (invert through origin)
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar):
        # True division of the vector by a scalar
        return Vector2D(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar):
        # One way to implement modulus operation: for each component
        return Vector2D(self.x % scalar, self.y % scalar)

    def __abs__(self):
        #Absolute value (magnitude, length) of the vector
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, other) -> float:
        # absolute distance between vectors self and other
        return abs(self - other)

    
    
