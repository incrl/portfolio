from scipy.ndimage import imread
import matplotlib.pyplot as plt
import numpy as np

filename = "..\WorkingData\BeforeProcessing_eslf.png"

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


#Plot light field by subappeture
appeture = np.zeros((rows, cols, ch))

for row in range(rows):
	for col in range(cols):
		r = (h*row) % rows + (h*row) / rows
		c = (w*col) % cols + (w*col) / cols
		appeture[row,col] = field[r,c]
		
im = appeture[:,:,0:3]
plt.imshow(im/255.0, vmin=0)
plt.show()