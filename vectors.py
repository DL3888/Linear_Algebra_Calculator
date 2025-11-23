


class Vector2d:
    '''This is a class for 2 dimensional vectors.'''
    def __init__(self, x = None, y = None, length = None):
        if length is not None and (x is None or y is None):
            self.length = length
            if x is None and y is not None:
                self.y = y
                self.x = (length ** 2 - y ** 2) ** 0.5
            elif y is None and x is not None:
                self.x = x
                self.y = (length ** 2 - x ** 2) ** 0.5
        elif length is None and (x is not None and y is not None):
            self.x = x
            self.y = y
            self.length = Vector2d.length(self)
        else:
            self.x = x
            self.y = y
            self.length = length

    @classmethod
    def zero(cls):
        return cls(0, 0)

    def __eq__(self, other):
        if isinstance(other, Vector2d):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __repr__(self):
        return "<{}, {}> with a length of {} units".format(self.x, self.y, self.length)

    def __add__(self, other):
        '''Simple vectors sum'''
        if isinstance(other, Vector2d):
            return Vector2d(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __mul__(self, k):
        '''Multiplication of vectors'''
        if isinstance(k, Vector2d):
            '''Here we simply call the dot-product function if the two arguments are 2 dimensional vectors'''
            return self.dotp(k)
        elif isinstance(k, (int, float)):
            '''Scalar multiplication'''
            return Vector2d(k * self.x, k * self.y)
        else:
            return NotImplemented

    def __rmul__(self, k):
        return self.__mul__(k)

    def dotp(self, other):
        '''Dot product'''
        if isinstance(other, Vector2d):
            return self.x * other.x + self.y * other.y
        else:
            return False

    def isPerpendicular(self, other):
        '''Explicit: Check if the two vectors are perpendicular'''
        if isinstance(other, Vector2d):
            return True if self.dotp(other) == 0 else False
        else:
            return False

    def length(self):
        '''Calculate the length (magnitude) of the provided vector'''
        return (self.x ** 2 + self.y ** 2) ** 0.5







class Vector3d(Vector2d):
    def __init__(self, x, y, z = None, length = None):
        super().__init__(x, y)
        self.z = z

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    def __eq__(self, other):
        if isinstance(other, Vector3d):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Vector3d):
            return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return NotImplemented

    def __repr__(self):
        return "<{}, {}, {}>".format(self.x, self.y, self.z)

    def __mul__(self, k):
        if isinstance(k, Vector3d):
            return self.dotp(k)
        elif isinstance(k, (int, float)):
            return Vector3d(k * self.x, k * self.y, k * self.z)
        else:
            return NotImplemented

    def __rmul__(self, k):
        return self.__mul__(k)

    def dotp(self, other):
        if isinstance(other, Vector3d):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return False

    def crossp(self, other):
        if isinstance(other, Vector3d):
            return Vector3d(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
        else:
            return False

    def isPerpendicular(self, other):
        if isinstance(other, Vector3d):
            return True if self.dotp(other) == 0 else False
        else: return False

    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
