import torch
from torch.autograd import Variable
import torchvision
import numpy as np
import torch.utils.data
from Unet import UNet
import time
from math import floor
from outputSaver import *
from refocuser import *


####################################Setting Parameters##################################
# topology = Topology of the network to train with
# split = Train/Test split (i.e. the number of images to include in the training set)

topology = 2  # 1 = CNN,  2 = UNet, 3 = CNN with BatchNorm
split = 700
learning_rate = 1e-4
b = 4 # Number of images per round
skip = 40 # Number of iterations before a print
use_whitening = False
num_epochs = 500
use_residual = False
use_delay = False
sub_epochs = 10 # Number of epochs with a residual penalty
res_factor = 1e-6 # Residual Factor

savedir = "D:\\Refocuser\\Results\\"
imagedir = "images\\"
descriptor = ""

####################################Needed Functions##################################
def pad(in_img):
	
	h,w = in_img.shape[1:3]
	
	h_pad = (16 - h % 16) % 16
	w_pad = (16 - w % 16) % 16

	result = np.pad(in_img, ((0,0),(0,h_pad),(0,w_pad),(0,0)), 'constant', constant_values=0)
	
	return result
	
# Composed Function
def unpadder(height,width):
	def unpad(image):
		return image[:,:,:height,:width]
	return unpad

def gradientMagnitude(batch_input):
	
	values = batch_input
	
	# Define neighborhood
	tl = values[:,:,0:-2,0:-2]
	top = values[:,:,0:-2,1:-1]
	tr = values[:,:,0:-2,2:]
	left = values[:,:,1:-1,0:-2]
	center = values[:,:,1:-1,1:-1]
	right = values[:,:,1:-1,2:]
	bl = values[:,:,2:,0:-2]
	bottom = values[:,:,2:,1:-1]
	br = values[:,:,2:,2:]
	
	# Sobel Kernel
	dx = -1 * tl + -2 * left + -1 * bl + 1 * tr + 2 * right + 1 * br
	dy = -1 * tl + -2 * top + -1 * tr + 1 * bl + 2 * bottom + 1 * br 
	
	mags = torch.sqrt(torch.mul(dx,dx) + torch.mul(dy,dy))
	
	# Scale mags to 0-1
	result = mags/torch.max(mags)
	
	return result
	
def residualPenalty(residual, batch_input):

	grads = gradientMagnitude(batch_input)

	#batch, ch, rows, cols = residual.shape
	
	values = residual
	
	#values = np.pad(values, ((0,0),(0,0),(1,1),(1,1)), "edge")
	
	# Define the neighborhood
	tl = values[:,:,0:-2,0:-2]
	top = values[:,:,0:-2,1:-1]
	tr = values[:,:,0:-2,2:]
	left = values[:,:,1:-1,0:-2]
	center = values[:,:,1:-1,1:-1]
	right = values[:,:,1:-1,2:]
	bl = values[:,:,2:,0:-2]
	bottom = values[:,:,2:,1:-1]
	br = values[:,:,2:,2:]
	
	d0 = tl - center
	d1 = top - center
	d2 = tr - center
	d3 = left - center
	d4 = right - center
	d5 = bl - center
	d6 = bottom - center
	d7 = br - center
	
	# Find the RGB distance to each neighbor
	result = torch.mul(d0,d0) + torch.mul(d1,d1) + torch.mul(d2,d2) + torch.mul(d3,d3) + torch.mul(d4,d4) + torch.mul(d5,d5) + torch.mul(d6,d6) + torch.mul(d7,d7)    
	
	thresh = .5
	weighting = torch.sigmoid(grads-thresh)
	
	# Weight based on the image gradient
	result = weighting*result
	
	# Add the color channels together and batches for a total penalty
	penalty = torch.sum(result)
	
	return penalty
	
	
####################################Loading Data##################################

filename_original = "D:\\LightFieldData\\Refocused\\refocused.npy"
filename_refocused = "D:\\LightFieldData\\Refocused\\original.npy"

original_data = np.load(filename_original).astype(np.float32)
refocused_data = np.load(filename_refocused).astype(np.float32)

_, orig_height, orig_width, _ =  original_data.shape

# Pad data for Unet
if topology == 2:
	original_data = pad(original_data)
	
unpad = unpadder(orig_height,orig_width)
	
# Reshape data for pytorch
original_data = np.transpose(original_data, (0,3,1,2))
refocused_data = np.transpose(refocused_data, (0,3,1,2))

# Put data between 0 and 1
original_data = original_data/255.0
refocused_data = refocused_data/255.0

# Train/Test split 
train_orig = original_data[:split]
train_refc = refocused_data[:split]
test_orig = original_data[split:]
test_refc = refocused_data[split:]

num_images, ch, height, width, = original_data.shape
print(original_data.shape)

####################################Model Definition##################################

if topology == 1:
	model = torch.nn.Sequential(
			torch.nn.Conv2d(3, 64, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 64, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 64, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 64, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 32, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(32, 16, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(16, 8, 3, stride=1, padding=1),
			torch.nn.ReLU(),
			torch.nn.Conv2d(8, 3, 3, stride=1, padding=1),
			torch.nn.Tanh()
		)

if topology == 2:
	model = UNet(3, depth=5)

if topology == 3:
	model = torch.nn.Sequential(
			torch.nn.Conv2d(3, 64, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(64),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 64, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(64),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 64, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(64),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 64, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(64),
			torch.nn.ReLU(),
			torch.nn.Conv2d(64, 32, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(32),
			torch.nn.ReLU(),
			torch.nn.Conv2d(32, 16, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(16),
			torch.nn.ReLU(),
			torch.nn.Conv2d(16, 8, 3, stride=1, padding=1),
			torch.nn.BatchNorm2d(8),
			torch.nn.ReLU(),
			torch.nn.Conv2d(8, 3, 3, stride=1, padding=1),
			torch.nn.Tanh()
		)
	
model.cuda()

loss_fn = torch.nn.MSELoss(size_average=True)
params = model.parameters()
optimizer = torch.optim.Adam(params, lr=learning_rate)

####################################Training The Network##################################
original_image = original_data[0:1]
refocused_image = refocused_data[0:1]
learned_images = []
residual_images = []

# Setup for visualization
current = Variable(torch.from_numpy(original_image), requires_grad=False).cuda()

original_image = unpad(original_image)

# Setup Dataloaders
train_data = torch.utils.data.TensorDataset(torch.from_numpy(train_orig), torch.from_numpy(train_refc))
train_loader = torch.utils.data.DataLoader(train_data, batch_size=b, shuffle=True)
test_data = torch.utils.data.TensorDataset(torch.from_numpy(test_orig), torch.from_numpy(test_refc))
test_loader = torch.utils.data.DataLoader(test_data, batch_size=b, shuffle=True)

mse_loss_vals = []
res_loss_vals = []
tot_loss_vals = []

if not use_residual:
	for epoch in range(num_epochs):

		if epoch == 0:
			start_time = time.time()

		print("Epoch", epoch)
		i = 0
		
		for batch_input, batch_output in train_loader:
			
			batch_input = Variable(batch_input,requires_grad=False).cuda()
			batch_output = Variable(batch_output,requires_grad=False).cuda()
			
			# Forward Pass
			result = model(batch_input)
			MSELoss = loss_fn(unpad(torch.clamp(result,0,1)), batch_output)
			loss = MSELoss
			
			# Training step
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()
			
			# Printing statement
			i += 1
			if i % skip == 0:
				print(i,loss.data[0])
				tot_loss_vals.append(loss.data[0])
			
		
		# Visualization of progress
		result = model(current)
		result = unpad(torch.clamp(result,0,1))
		learned_images.append(result.data.cpu().numpy())
		
		# Print estimated time of completion
		if epoch==0:
			end_time = time.time()
			num_seconds = end_time-start_time
			estimation = num_seconds*(num_epochs+sub_epochs)
			print("\n")
			print("Estimated Time of Completion: " + str(floor(estimation/3600)) + " hours and " + str(floor((estimation % 3600) /60 )) + " minutes")
			print("\n")

else:
	for epoch in range(num_epochs):

		if epoch == 0:
			start_time = time.time()

		print("Epoch", epoch)
		i = 0
		
		for batch_input, batch_output in train_loader:
			
			batch_input = Variable(batch_input,requires_grad=False).cuda()
			batch_output = Variable(batch_output,requires_grad=False).cuda()
			
			# Forward Pass
			residual = model(batch_input)
			MSELoss = loss_fn(unpad(torch.clamp(batch_input + residual,0,1)), batch_output)
			loss = MSELoss
			
			# Training step
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()
			
			# Printing statement
			i += 1
			if i % skip == 0:
				print(i,loss.data[0])
				tot_loss_vals.append(loss.data[0])
			
		
		# Visualization of progress
		residual = model(current)
		result = torch.clamp(residual + current,0,1)
		residual_images.append(unpad(residual).data.cpu().numpy())
		learned_images.append(unpad(result).data.cpu().numpy())
		
		# Print estimated time of completion
		if epoch==0:
			end_time = time.time()
			num_seconds = end_time-start_time
			estimation = num_seconds*(num_epochs+sub_epochs)
			print("\n")
			print("Estimated Time of Completion: " + str(floor(estimation/3600)) + " hours and " + str(floor((estimation % 3600) /60 )) + " minutes")
			print("\n")

	if use_delay:		
		for epoch in range(sub_epochs):

			print("Epoch", epoch)
			i = 0
			
			for batch_input, batch_output in train_loader:
				
				batch_input = Variable(batch_input,requires_grad=False).cuda()
				batch_output = Variable(batch_output,requires_grad=False).cuda()
				
				# Forward Pass
				residual = model(batch_input)
				residualLoss = res_factor * residualPenalty(unpad(residual), unpad(batch_input))
				MSELoss = loss_fn(unpad(torch.clamp(batch_input + residual,0,1)), batch_output)
				loss = MSELoss + residualLoss
				
				# Training step
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()
				
				# Printing statement
				i += 1
				if i % skip == 0:
					print(i,loss.data[0],MSELoss.data[0],residualLoss.data[0])
					tot_loss_vals.append(loss.data[0])
					mse_loss_vals.append(MSELoss.data[0])
					res_loss_vals.append(residualLoss.data[0])
				
			
			# Visualization of progress
			residual = model(current)
			result = torch.clamp(residual + current,0,1)
			residual_images.append(unpad(residual).data.cpu().numpy())
			learned_images.append(unpad(result).data.cpu().numpy())
		
##########################################Saving Output######################################
print("Saving...")

# Make saving directory
directory = savedir + makeName(topology,split,b,descriptor)
ensure_dir(directory)

# Save the final trained model
saveModel(model,directory)

# Save all the images
saveImages(original_image, refocused_image, learned_images, directory)

# Save learning steps as mp4	
saveMP4(residual_images, directory, "residual.mp4", residual=True)
saveMP4(learned_images, directory, "result.mp4")

# Save Loss Graphs
saveLoss(tot_loss_vals,mse_loss_vals,res_loss_vals,directory)

# Log Parameters
saveLog(topology, split, learning_rate, b, use_whitening, num_epochs, use_residual, use_delay, sub_epochs, res_factor, directory)
print("Done")

# Automatically test on unknown output
print("Auto Testing...")
refocusDirectory(model,imagedir,directory)
print("Done")
