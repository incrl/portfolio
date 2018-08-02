import os
import numpy as np
from scipy.misc import imsave, imread
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import torch
from torch.autograd import Variable

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
		
def makeName(topology, b, epochs, descriptor=""):
	if topology == 1:
		text = "Simple_CNN"
	if topology == 2:
		text = "Unet_Architecture"
	if topology == 3:
		text = "Unet_3D_Convolution"
	if topology == 4:
		text = "EncodeDecode_3D_Convolution"
	if topology == 5:
		text = "Conditional_Instance_Norm"
	if topology == 6:
		text = "myResNet18"
	return text + "Batch" + str(b) + "Epochs" + str(epochs) + descriptor + "\\"

def saveModel(model, directory="", fn="trained_model.pt"):
	torch.save(model, directory+fn)
	
def saveLoss(train_loss,test_loss=None,directory=""):
	np.save(directory+"training_loss",np.array(train_loss))
	fig, ax = plt.subplots(1, 1)
	plt.plot(train_loss)
	plt.savefig(directory+"training_loss.png", dpi=960, bbox_inches="tight")
	
	if test_loss:
		np.save(directory+"testing_loss",np.array(test_loss))
		fig, ax = plt.subplots(1, 1)
		plt.plot(test_loss)
		plt.savefig(directory+"testing_loss.png", dpi=960, bbox_inches="tight")
	
def compareStacks(stack_truth, stack_predicted, numpy=False):
	
	# Switch from Torch to Numpy if needed
	if not numpy:
		stack_truth = stack_truth.data.cpu().numpy()
		stack_truth = np.transpose(stack_truth,(0,2,3,1))
	
		stack_predicted = stack_predicted.data.cpu().numpy()
		stack_predicted = np.transpose(stack_predicted,(0,2,3,1))
	
	num, rows, cols, ch = stack_truth.shape
	
	width = num * cols
	height = 3 * rows
	
	result = np.zeros((height,width,ch))
	
	# 1st Row
	for i in range(num):
		result[0:rows,i*cols:(i+1)*cols] = stack_truth[i]
		
	# 2nd Row
	for i in range(num):
		result[1*rows:2*rows,i*cols:(i+1)*cols] = stack_predicted[i]
		
	# 3rd Row
	for i in range(num):
		result[2*rows:3*rows,i*cols:(i+1)*cols] = (stack_truth[i] - stack_predicted[i] + 1)/2
		
	return result
	
def stackViewer(stack, numpy = False):
	
	# Switch from Torch to Numpy if needed
	if not numpy:
		stack = stack.data.cpu().numpy()
		stack = np.transpose(stack,(0,2,3,1))
		
	num, rows, cols, ch = stack.shape
	
	# Assumption: The stack is symmetric
	half = int(num/2)
	width = num * cols
	height = 2 * rows
	
	result = np.zeros((height,width,ch))
	
	# 1st Row
	for i in range(num):
		result[0:rows,i*cols:(i+1)*cols] = stack[i]
		
	val_min = np.amin(stack[[half]] - stack)
	val_max = np.amax(stack[[half]] - stack)
		
	# 2nd Row
	for i in range(num):

		value = (stack[half] - stack[i] + 1)/2
		
		# Scale for visibility
		result[1*rows:2*rows,i*cols:(i+1)*cols] = (1.0/(val_max - val_min))*(value - val_min) 
		
	return result

def saveMP4(the_images, directory="", fn="view.mp4", residual=False):
	mp4Writer = animation.writers['ffmpeg']
	the_writer = mp4Writer(fps=30, metadata=dict(artist='Me'))
	fig = plt.figure()
	ims = []

	plt.axis('off')

	for image in the_images:
		image = np.transpose(image,(0,2,3,1))
		if residual:
			image = np.clip((image+1)/2.0,0.0,1.0)[0]
		else:
			image = image[0]
		ims.append([plt.imshow(image,vmin=0.0,vmax=1.0,animated=True)])
		
	im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)
	im_ani.save(directory + fn, writer=the_writer)
	
def refocuser(model, filename, directory="", ImageNet=False):

	# Load image to refocus
	image_orig = imread(filename).astype(np.float32)
	orig_height, orig_width, _ = image_orig.shape

	# Make pytorch friendly
	image = np.expand_dims(image_orig,axis=0)

	# Put in range 0-1
	image = image/255.0
	
	# Make Pytorch friendly
	image = np.transpose(image, (0,3,1,2))
	
	# Make ImageNet Friendly
	if ImageNet:
		# Subtract ImageNet Means
		image[:,0,:,:] -= 0.48501961
		image[:,1,:,:] -= 0.45795686
		image[:,2,:,:] -= 0.40760392

		# Take appropriate crop
		crop_size = 224
		_,_, rows, cols = image.shape
		r = np.random.randint(0,rows-crop_size)
		c = np.random.randint(0,cols-crop_size)
		image = image[:,:,r:r+crop_size,c:c+crop_size]
	
	data = Variable(torch.from_numpy(image), requires_grad=False, volatile=True).cuda()
	
	# Feed through to get result
	model.eval()
	result = model(data)[0]
	
	# Undo ImageNet stuff
	if ImageNet:
		result[:,0,:,:] = result[:,0,:,:] + 0.48501961
		result[:,1,:,:] = result[:,0,:,:] + 0.45795686
		result[:,2,:,:] = result[:,0,:,:] + 0.40760392
	
	
	# Make stack comparison image
	stack = stackViewer(result)
	
	# Remove extension from filename for saving
	fn = filename.split("\\")[-1]
	name = fn.split(".")[0]
	imsave(directory+name+"_stack.png",stack)
	
def refocuser2(model, filename, directory=""):

	# Load image to refocus
	image_orig = imread(filename).astype(np.float32)
	orig_height, orig_width, _ = image_orig.shape

	# Make pytorch friendly
	image = np.expand_dims(image_orig,axis=0)

	# Put in range 0-1
	image = image/255.0
	
	# Make Pytorch friendly
	image = np.transpose(image, (0,3,1,2))
	data = Variable(torch.from_numpy(image), requires_grad=False, volatile=True).cuda()
	
	# Feed through to get result
	model.eval()
	result1 = model(data,[1,0,0,0,0])
	result2 = model(data,[0,1,0,0,0])
	result3 = model(data,[0,0,1,0,0])
	result4 = model(data,[0,0,0,1,0])
	result5 = model(data,[0,0,0,0,1])
	result = torch.cat((result1,result2,result3,result4,result5),1)[0]
	
	# Make stack comparison image
	stack = stackViewer(result)
	
	# Remove extension from filename for saving
	fn = filename.split("\\")[-1]
	name = fn.split(".")[0]
	imsave(directory+name+"_stack.png",stack)
	
def refocusDirectory(model, input_directory, output_directory="", ImageNet=False):
	import os
	files = os.listdir(input_directory)
	for f in files:
		refocuser(model,input_directory+f,output_directory, ImageNet)
		
def refocusDirectory2(model, input_directory, output_directory=""):
	import os
	files = os.listdir(input_directory)
	for f in files:
		refocuser2(model,input_directory+f,output_directory)
