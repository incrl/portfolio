load_directory = "D:\\LightFieldData\\FocalNPY\\"
save_directory = "D:\\LightFieldData\\FocalViews\\"

import os
import numpy as np
from scipy.misc import imsave
from tqdm import trange, tqdm

files = os.listdir(load_directory)

for i in trange(0,int(len(files))):

	file = files[i]

	stack = np.load(load_directory+file)

	num, rows, cols, ch = stack.shape
	
	# Assumption: The stack is symmetric
	half = int(num/2)
	width = half * cols
	height = 3 * rows
	
	result = np.zeros((height,width,ch))
	
	# Nearer Focal Lengths
	for i in range(half):
		result[0:rows,i*cols:(i+1)*cols] = stack[i]
	
	# Original
	result[rows:2*rows,int(width/2)-int(cols/2):int(width/2)+int(cols/2)] = stack[half]
	
	# Farther Focal Lengths
	for i in range(half):
		result[2*rows:3*rows,i*cols:(i+1)*cols] = stack[i+half+1]

	# Remove extension from file name
	extension = len(file.split(".")[-1])
	name = file[0:-(extension+1)]
	
	imsave(save_directory + name + ".png", result) 

