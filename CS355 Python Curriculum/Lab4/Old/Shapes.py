
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
		#To be implemented
		return None
		
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
		#To be implemented
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
		#To be implemented
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
		#To be implemented
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
		#To be implemented
		return False
