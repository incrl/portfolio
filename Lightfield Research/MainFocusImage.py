from scipy.ndimage import imread
import matplotlib.pyplot as plt
import numpy as np

filename = "..\..\WorkingData\Pic2WB2_eslf.png"

field = imread(filename)
print field.dtype
im = field[:,:,0:3]

#Specify appeture height and width
h = 14
w = 14

#Plot original light field
plt.imshow(im, vmin=0)
plt.show()

rows, cols, ch = np.shape(field)


#Plot original focus image

#Find it's physical size
im_h = rows/h
im_w = cols/w

original = np.zeros((im_h, im_w, ch-1))

for y in range(im_h):
	for x in range(im_w):
		count = 0
		result = [0,0,0]
		for row in range(h):
			for col in range(w):
				r = row + y*h
				c = col + x*w
				if field[r,c,3] != 0:
					count += 1
					result += field[r,c,0:3]

		#print "Result:", result
		#print "Count:", count
		original[y,x] = result/count
		
plt.imshow(original/255.0, vmin=0, vmax=1)
plt.show()		
