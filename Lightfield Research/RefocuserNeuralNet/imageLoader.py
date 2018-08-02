load_directory = "D:\\LightFieldData\\Focal\\"
save_directory = "D:\\LightFieldData\\FocalNPY\\" #This directory must already exsist

import os
from scipy.misc import imread
from tqdm import trange, tqdm
import numpy as np

# Crop Size
c, r = 540, 375

folders = os.listdir(load_directory)

files = os.listdir(load_directory + "\\" + folders[0])
for file in tqdm(files):
	images = []
	for folder in folders:
		im = imread(load_directory + "\\" + folder + "\\" + file).astype(np.float32)[:r,:c]
		images.append(im)
	
	images = np.array(images)/255.0
	
	# Remove extension from file name
	extension = len(file.split(".")[-1])
	name = file[0:-(extension+1)]
	
	np.save(save_directory+name,images)