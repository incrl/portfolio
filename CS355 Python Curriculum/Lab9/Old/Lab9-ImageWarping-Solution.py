from scipy.ndimage import imread
import matplotlib.pyplot as plt
import numpy as np

tv = imread('tv.jpg')
plt.imshow(tv,cmap="Greys_r",vmin=0)
plt.show()

cat = imread('cat.jpg')

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
		
def interpolate(data, x, y):

	#Get the four corners to interpolate between
	row = int(y)
	col = int(x)
	try:
		tl = data[row-1,col-1]
		tr = data[row-1,col]
		bl = data[row, col-1]
		br = data[row,col]
	except:
		return data[row,col]
	
	#Get the x and y difference
	dx = x % 1
	dy = y % 1
	
	#Interpolate the sides
	l = dy*tl + (1 - dy)*bl
	r = dy*tr + (1 - dy)*br
	
	#Interpolate to point
	return dx*l + (1-dx)*r
	
		
def getHomography(s0,s1,s2,s3,t0,t1,t2,t3):

    x0s = s0.x
    y0s = s0.y
    x0t = t0.x
    y0t = t0.y

    x1s = s1.x
    y1s = s1.y
    x1t = t1.x
    y1t = t1.y

    x2s = s2.x
    y2s = s2.y
    x2t = t2.x
    y2t = t2.y

    x3s = s3.x
    y3s = s3.y
    x3t = t3.x
    y3t = t3.y

    #Solve for the homography matrix
    A = np.matrix([
            [x0s, y0s, 1, 0, 0, 0, -x0t*x0s, -x0t*y0s],
            [0, 0, 0, x0s, y0s, 1, -y0t*x0s, -y0t*y0s],
            [x1s, y1s, 1, 0, 0, 0, -x1t*x1s, -x1t*y1s],
            [0, 0, 0, x1s, y1s, 1, -y1t*x1s, -y1t*y1s],
            [x2s, y2s, 1, 0, 0, 0, -x2t*x2s, -x2t*y2s],
            [0, 0, 0, x2s, y2s, 1, -y2t*x2s, -y2t*y2s],
            [x3s, y3s, 1, 0, 0, 0, -x3t*x3s, -x3t*y3s],
            [0, 0, 0, x3s, y3s, 1, -y3t*x3s, -y3t*y3s]
        ])

    b = np.matrix([
            [x0t],
            [y0t],
            [x1t],
            [y1t],
            [x2t],
            [y2t],
            [x3t],
            [y3t]
        ])

    #The homorgraphy solutions a-h
    solutions = np.linalg.solve(A,b)

    solutions = np.append(solutions,[[1.0]], axis=0)

    #Reshape the homography into the appropriate 3x3 matrix
    homography = np.reshape(solutions, (3,3))
    
    return homography

homography = getHomography(s0,s1,s2,s3,t0,t1,t2,t3)
invHomography = np.linalg.inv(homography)

for pt in screen:
	h_pt = np.matrix([[pt.x],[pt.y],[1]])
	c_pt = invHomography*h_pt
	x = c_pt[0]/c_pt[2]
	y = c_pt[1]/c_pt[2]
	
	tv[pt.y,pt.x]=cat[int(y),int(x)]
	
plt.imshow(tv,cmap="Greys_r",vmin=0)
plt.show()


###########Whiteboard code#################3
board = imread('whiteboard.jpg')[:,:,0]
plt.imshow(board,cmap="Greys_r",vmin=0)
plt.show()

s0 = Point(20,14)
s1 = Point(660,87)
s2 = Point(660,271)
s3 = Point(17, 331)

t0 = Point(0,0)
t1 = Point(400,0)
t2 = Point(400,200)
t3 = Point(0,200)

result = np.zeros((199,399))

homography = getHomography(s0,s1,s2,s3,t0,t1,t2,t3)
invHomography = np.linalg.inv(homography)

for row in range(0,len(result)):
	for col in range(0,len(result[0])):
		h_pt = np.matrix([[col],[row],[1]])
		c_pt = invHomography*h_pt
		x = c_pt[0]/c_pt[2]
		y = c_pt[1]/c_pt[2]
		
		result[row,col] = interpolate(board, x, y)

plt.imshow(result,cmap="Greys_r",vmin=0)
plt.show()
