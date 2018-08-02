import torch
import numpy as np
from torch.autograd import Variable
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt

def pad(in_img):
	
	h,w = in_img.shape[1:3]
	
	h_pad = (16 - h % 16) % 16
	w_pad = (16 - w % 16) % 16

	result = np.pad(in_img, ((0,0),(0,h_pad),(0,w_pad),(0,0)), 'constant', constant_values=0)
	
	return result

def refocuser(model, filename, directory=""):

	# Load image to refocus
	image_orig = imread(filename).astype(np.float32)
	orig_height, orig_width, _ = image_orig.shape

	# Make pytorch friendly
	image = np.expand_dims(image_orig,axis=0)

	# Pad for UNet
	image = pad(image)
	
	# Put in range 0-1
	image = image/255.0
	
	# Make Pytorch friendly
	image = np.transpose(image, (0,3,1,2))
	data = Variable(torch.from_numpy(image), requires_grad=False).cuda()

	# Feed through to get result
	residual = model(data)
	result = residual + data
	final = result.data.cpu().numpy()

	#Crop to original size
	final = final[:,:,:orig_height,:orig_width]

	final = np.transpose(final,(0,2,3,1))
	final = np.clip(final,0.0,1.0)[0]
	
	# Remove extension from filename for saving
	fn = filename.split("\\")[-1]
	name = fn.split(".")[0]
	imsave(directory+name+"_refocused.png",final)
	
	# Add original for comparison convenience
	imsave(directory+fn, image_orig)
	
def refocusDirectory(model, input_directory, output_directory=""):
	import os
	files = os.listdir(input_directory)
	for f in files:
		refocuser(model,input_directory+f,output_directory)
