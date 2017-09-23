from scipy.ndimage import imread
import matplotlib.pyplot as plt
import numpy as np

tv = imread('tv.jpg')
plt.imshow(tv,cmap="Greys_r",vmin=0)
plt.show()

cat = imread('cat.jpg')
plt.imshow(cat,cmap="Greys_r",vmin=0)
plt.show()

class Point():
	def __init__(self,x,y):
		self.x = x
		self.y = y

s0 = Point(0,0)
s1 = Point(255,0)
s2 = Point(255,255)
s3 = Point(0, 255)

t0 = Point(245,152)
t1 = Point(349,150)
t2 = Point(349,253)
t3 = Point(246,261)

def getScreen():
	result = []
	screen = np.loadtxt("screen.txt")
	for line in screen:
		result.append(Point(int(line[0]), int(line[1])))
	return result
	
screen = getScreen()