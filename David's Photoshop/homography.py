import numpy as np

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

def interpolate(image, x, y):
    
    rows,cols,_ = image.shape
    
    if x<0 or x>cols-1 or y<0 or y>rows-1:
        return [0,0,0]
    
    #Get the four corners to interpolate between
    row = int(y)
    col = int(x)
    try:
        tl = image[row,col]
        tr = image[row,col+1]
        bl = image[row+1,col]
        br = image[row+1,col+1]
    except:
        return image[row,col]

    #Get the x and y decimal
    dx = x - col
    dy = y - row
    
    #Interpolate the sides
    left = (1-dy)*tl + dy*bl
    right = (1-dy)*tr + dy*br
    
    #Interpolate to point
    return (1-dx)*left + dx*right

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
	
    
def getCanvas(t0, t1, t2, t3):
    
    #Make bounding box
    left = min(t0.x, t1.x, t2.x, t3.x)
    right = max(t0.x, t1.x, t2.x, t3.x)
    top = min(t0.y, t1.y, t2.y, t3.y)
    bottom = max(t0.y, t1.y, t2.y, t3.y)
    
    xvals = range(left,right+1)
    yvals = range(top,bottom+1)
    
    return (xvals,yvals)