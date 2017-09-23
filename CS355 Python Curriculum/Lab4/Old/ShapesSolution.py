import numpy as np
from math import sin
from math import cos
from math import sqrt
from math import pi

class Point:
	
	def __init__(self,x,y):
		self.x = x
		self.y = y

#Abstract Class
class Shape:
	
	def pointInShape(self, pt, tolerance):
		pass

	def getWidth(self):
		pass
	
	def getHeight(self):
		pass
		
	def worldToObject(self, pt):
		translate = np.matrix([[1, 0, -self.center.x], [0, 1, -self.center.y], [0, 0, 1]])
		rotate = np.matrix([[cos(self.rotation * pi/180.0), sin(self.rotation* pi/180.0), 0], [-sin(self.rotation* pi/180.0), cos(self.rotation* pi/180.0), 0], [0, 0, 1]])
		h_pt = np.matrix([[pt.x],[pt.y],[1]])
		o_pt = rotate*translate*h_pt
		
		return Point(o_pt[0,0], o_pt[1,0])

class Rect(Shape):
	
	def __init__(self, color, center, width, height):
		self.color = color
		self.rotation = 0.0
		self.center = center
		self.width = width
		self.height = height
		
	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height
		
	def pointInShape(self, pt, tolerance):
		pt = self.worldToObject(pt)
		if pt.x >= -self.width/2.0 and pt.x <= self.width/2.0:
			if pt.y >= -self.height/2.0 and pt.y <= self.height/2.0:
				return True
		
		return False

class Square(Shape):
	
	def __init__(self, color, center, size):
		self.color = color
		self.rotation = 0.0
		self.center = center
		self.size = size
		
	def getWidth(self):
		return self.size
		
	def getHeight(self):
		return self.size
		
	def pointInShape(self, pt, tolerance):
		pt = self.worldToObject(pt)
		if pt.x >= -self.size/2.0 and pt.x <= self.size/2.0:
			if pt.y >= -self.size/2.0 and pt.y <= self.size/2.0:
				return True
				
		return False
		
class Ellipse(Shape):
	
	def __init__(self, color, center, width, height):
		self.color = color
		self.rotation = 0.0
		self.center = center
		self.width = width
		self.height = height
		
	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height
		
	def pointInShape(self, pt, tolerance):
		
		a = self.width/2
		b = self.height/2
		
		pt = self.worldToObject(pt)
		if (pt.x**2)/(a**2) + (pt.y**2)/(b**2) <= 1:
			return True
		
		return False
		
class Circle(Shape):
	
	def __init__(self, color, center, radius):
		self.color = color
		self.rotation = 0.0
		self.center = center
		self.radius = radius
		
	def getWidth(self):
		return 2*self.radius
		
	def getHeight(self):
		return 2*self.radius
		
	def pointInShape(self, pt, tolerance):
		pt = self.worldToObject(pt)
		if pt.x**2 + pt.y**2 <= self.radius**2:
			return True
			
		return False
