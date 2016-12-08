import math

class Vector2(object):
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "(%s, %s)" % (self.x, self.y)
		
	@classmethod
	def from_points(cls, P1, P2):
		return cls(P2[0] - P1[0], P2[1] - P1[1])
		
	def get_magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
		
	def normalize(self):
		magnitude = self.get_magnitude()
		self.x /= magnitude
		self.y /= magnitude
		
		
A = (10.0, 20.0)
B = (30.0, 35.0)
AB = Vector2.from_points(A, B)
print("Vector AB is {}".format(AB))
print("Magnitude of Vector AB is {}".format(AB.get_magnitude()))
AB.normalize()
print("Vector AB normalized is {}".format(AB))
