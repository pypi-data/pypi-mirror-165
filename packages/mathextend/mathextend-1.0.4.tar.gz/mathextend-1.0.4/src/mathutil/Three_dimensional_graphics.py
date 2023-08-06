from src.mathutil.Flat_graphics import *

INFINITE_GREATNESS = 10

for i in range(5):
    INFINITE_GREATNESS **= 10


class Three_dimensional_graphics:
    def __init__(self):
        pass


class Cylinder(Three_dimensional_graphics):
    def __init__(self, underside, height):
        super().__init__()
        if isinstance(underside, (Circle, Triangle, Rectangle)) and height and isinstance(height, (int, float)):
            self._Underside = underside
            if height >= INFINITE_GREATNESS:
                raise ValueError('The height is too high.')
            else:
                self._height = height
        else:
            raise ValueError('The height must be a floating-point or integer number and not be 0.')
    
    @property
    def volume(self):
        return self._Underside.area * self._height
    
    @property
    def surface_area(self):
        return 2 * self._Underside.area + self._Underside.circumference * self._height
    
    def set_all(self, underside, height):
        if isinstance(underside, Rectangle) and height and isinstance(height, (int, float)):
            self._Underside = underside
            if height >= INFINITE_GREATNESS:
                raise ValueError('The height is too high.')
            else:
                self._height = height
        else:
            raise ValueError('The height must be a floating-point or integer number and not be 0.')
    
    @property
    def inspect(self) -> tuple:
        return self._Underside, self._height


class Sphere(Circle):
    def __init__(self, radius, pi=3.14):
        super().__init__(radius, pi)
    
    def set_all(self, radius, pi):
        super().set_all(radius, pi)
    
    def inspect(self):
        super().inspect()
    
    @property
    def volume(self):
        return super().area * super()._radius
    
    @property
    def surface_area(self):
        return super().area ** 2
    
    @property
    def inspect(self) -> tuple:
        return super().inspect()


class Cone(Three_dimensional_graphics):
    def __init__(self, underside, height):
        super().__init__()
        if isinstance(underside, Circle):
            if height == 0:
                raise ValueError("Height can't be 0.")
            elif height >= INFINITE_GREATNESS:
                raise ValueError('The height is too high.')
            else:
                self._underside = underside
                self._height = height
        else:
            raise TypeError('Underside must be Circle.')
    
    def set_all(self, underside, height):
        self.__init__(underside, height)
    
    @property
    def volume(self):
        return Cylinder(self._underside, self._height).volume / 3
    
    @property
    def inspect(self) -> tuple:
        return self._underside, self._height

