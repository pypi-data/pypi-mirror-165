class Flat_graphics:
	def __init__(self):
		pass


class Rectangle(Flat_graphics):
	_width: int or float
	_height: int or float
	
	def __init__(self, width: int or float, height: int or float) -> None:
		super().__init__()
		if width == 0 or height == 0:
			raise ValueError("The width and height of the rectangle can't be 0.")
		elif isinstance(width, (int, float)) and isinstance(height, (int, float)):
			self._width = width
			self._height = height
		else:
			raise ValueError('The width and height of a rectangle must be a floating-point or integer number.')
	
	@property
	def area(self):
		width = self._width
		height = self._height
		return width * height
	
	def set_width(self, new_width: int or float) -> None:
		self._width = new_width
	
	def set_height(self, new_height: int or float) -> None:
		self._height = new_height
	
	@property
	def inspect(self) -> tuple:
		return self._width, self._height
	
	@property
	def circumference(self):
		return (self._width + self._height) * 2


class Triangle(Flat_graphics):
	_a: int or float
	_b: int or float
	_c: int or float
	
	def __init__(self, a: int or float, b: int or float, c: int or float):
		super().__init__()
		if a + b > c and a + c > b and b + c > a:
			self._a = a
			self._b = b
			self._c = c
		else:
			raise ValueError('The sum of any two sides of a triangle id greater than the third side.')
	
	@property
	def area(self):
		from math import sqrt
		s = (self._a + self._b + self._c) / 2
		return sqrt(s * (s - self._a) * (s - self._b) * (s - self._c))
	
	@property
	def inspect(self):
		return self._a, self._b, self._c
	
	def set_all(self, a, b, c):
		self._a = a
		self._b = b
		self._c = c
	
	@property
	def circumference(self):
		return self._a + self._b + self._c


class Circle(Flat_graphics):
	def __init__(self, radius, pi=3.14):
		super().__init__()
		if radius == 0:
			raise ValueError("The radius can't be 0.")
		elif not isinstance(radius, (int, float)):
			raise ValueError('The radius must be a floating-point or integer number.')
		elif not isinstance(pi, (int, float)):
			raise ValueError('Pi must be floating-point or integer numbers.')
		self._radius = radius
		self._diameter = radius * 2
		self._pi = pi
	
	def set_all(self, radius, pi):
		self._radius = radius
		self._pi = pi
	
	@property
	def area(self):
		return self._pi * self._radius ** 2
	
	@property
	def circumference(self):
		return self._pi * self._diameter
	
	def inspect(self):
		return self._radius, self._diameter, self._pi
