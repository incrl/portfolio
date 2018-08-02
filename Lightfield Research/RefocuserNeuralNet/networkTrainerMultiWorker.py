import torch
from torch.autograd import Variable
import torchvision
import numpy as np
from torch.utils.data import Dataset, DataLoader
import time
import os
from math import floor
from outputSaver import *
from myModules import *
from torch.optim.lr_scheduler import StepLR

###################################Additional Functions#################################]

def divergence(stack):
	
	batch,num,rows,cols,ch = stack.size()
	
	middle = num//2
	
	middle_image = stack[:,[middle],:,:,:]
	
	# Subtract the middle_image from the rest of the focal stack
	diff = stack - middle_image
	
	# Take RGB distance
	result = diff[:,:,0,:,:]**2 + diff[:,:,1,:,:]**2 + diff[:,:,2,:,:]**2
	
	# Sum along focal stack dimension
	result = result.sum(1)
	
	return result
	
def focalPenalty(stack,prediction):

	w0 = divergence(stack)
	w1 = divergence(prediction)
	
	result = (w0-w1)**2
	
	return result.sum()

####################################Loading Data##################################

class FocalStackDataset(Dataset):

	def __init__(self, root_dir, stack_size=5, ImageNet = False,reflections=False):

		self.root_dir = root_dir
		self.files = os.listdir(root_dir)
		self.num_files = len(self.files)
		self.stack_size=stack_size
		self.reflections = reflections
		self.ImageNet = ImageNet
		
		# Load one file to get the set size
		file_name = os.path.join(self.root_dir,self.files[0])
		stack = np.load(file_name)
		self.set_size = stack.shape[0]
		
		# Determine the number of augmentations that will occur on the dataset
		self.num_augments = (self.set_size-self.stack_size+1)
		if self.reflections:
			self.num_augments *= 4
		
	def __len__(self):
		return self.num_files*self.num_augments

	def __getitem__(self, idx):
		file_name = os.path.join(self.root_dir,self.files[idx % self.num_files])
		stack = np.load(file_name)
		
		# Move up the focal stack to augment data
		start = int(idx/self.num_files) % self.set_size
		
		middle = start + int(self.stack_size/2)
		original = stack[middle]
		stack = stack[start:start+self.stack_size]

		# Reflect the data over the x and y axis to augment the data
		if self.reflections:
			version = int(int(idx/self.num_files)/self.set_size)
			
			if version == 0:
				None # Don't reflect
			elif version == 1:
				original = original[::-1,:,:]
				stack = stack[:,::-1,:,:]
			elif version == 2:
				original = original[:,::-1,:]
				stack = stack[:,:,::-1,:]
			elif version == 3:
				original = original[::-1,::-1,:]
				stack = stack[:,::-1,::-1,:]
		
		# Put into pytorch format
		original = np.transpose(original,((2,0,1)))
		stack = np.transpose(stack,((0,3,1,2)))
		
		if self.ImageNet:
			# Subtract ImageNet Means
			original[0,:,:] -= 0.48501961
			original[1,:,:] -= 0.45795686
			original[2,:,:] -= 0.40760392
			stack[:,0,:,:] -= 0.48501961
			stack[:,1,:,:] -= 0.45795686
			stack[:,2,:,:] -= 0.40760392
		
			# Take appropriate crop
			crop_size = 224
			_, rows, cols = original.shape
			r = np.random.randint(0,rows-crop_size)
			c = np.random.randint(0,cols-crop_size)
			original = original[:,r:r+crop_size,c:c+crop_size]
			stack = stack[:,:,r:r+crop_size,c:c+crop_size]
		
		# Load the data
		sample = {'original': torch.from_numpy(original), 'stack': torch.from_numpy(stack)}

		return sample


if __name__ == "__main__":

	####################################Setting Parameters##################################
	# topology = Topology of the network to train with
	# split = Train/Test split (i.e. the number of images to include in the training set)

	topology = 2
	ImageNet = True
	learning_rate = 1e-4
	b = 8 # Number of images per round
	skip = 20 # Number of iterations before a print
	num_epochs = 2000
	num_lrs = 2
	alpha = 0

	#train_directory = "C:\\Users\\david\\Documents\\FocalNPY\\ConvergenceTest"
	#test_directory = "C:\\Users\\david\\Documents\\FocalNPY\\ConvergenceTest"
	train_directory = "C:\\Users\\david\\Documents\\FocalNPY\\Train"
	test_directory = "C:\\Users\\david\\Documents\\FocalNPY\\Test"

	#train_directory = "D:\\David\\LightFieldData\\FocalNPY\\ConvergenceTest"
	#test_directory = "D:\\David\\LightFieldData\\FocalNPY\\ConvergenceTest"
	#train_directory = "D:\\David\\LightFieldData\\FocalNPY\\Train"
	#test_directory = "D:\\David\\LightFieldData\\FocalNPY\\Test"


	savedir = "D:\\David\\Refocuser\\Results\\"
	imagedir = "images\\"
	descriptor = "FinalTry"


	# Setup Dataloaders
	train_data = FocalStackDataset(train_directory,ImageNet=ImageNet)
	train_loader = DataLoader(train_data, batch_size=b, shuffle=True, num_workers=2)
	test_data = FocalStackDataset(test_directory,ImageNet=ImageNet)
	test_loader = DataLoader(test_data, batch_size=b, shuffle=True, num_workers=2)

	###########################################Model Training#########################################


	if topology == 1:
		model = SimpleModel() 

	if topology == 2:
		model = SimpleUnet() 
		
	if topology == 3:
		model = Unet3D()
		
	if topology == 4:
		model = EncodeDecode3D()
		
	if topology == 5:
		model = ConditionalInstanceNorm()
		
	if topology == 6:
		model = myResNet18() 
		
	model.cuda()
		
	loss_fn = torch.nn.MSELoss(size_average=True)
	params = model.parameters()
	optimizer = torch.optim.Adam(params, lr=learning_rate)

	scheduler = StepLR(optimizer, num_epochs//num_lrs, gamma=0.1) 

	train_loss = []
	test_loss = []

	for epoch in range(num_epochs):

		if epoch == 0:
				start_time = time.time()

		print("Epoch", epoch)
		i = 0

		model.train()
		scheduler.step()
		for batch in train_loader:
			
			batch_input = batch["original"]
			batch_output = batch["stack"]
			
			batch_input = Variable(batch_input,requires_grad=False).cuda()
			batch_output = Variable(batch_output,requires_grad=False).cuda()
		
			# Forward Pass
			result = model(batch_input)
			MSELoss = loss_fn(result, batch_output)
			#PriorLoss = alpha * focalPenalty(batch_output, result) 
			loss = MSELoss #+ PriorLoss
			
			# Training step
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()
		
			# Printing statement
			i += 1
			if i % skip == 0:
				print(i,MSELoss.data[0])#,PriorLoss.data[0],loss.data[0])
				train_loss.append(loss.data[0])
			
		
		# Test entire testing set
		total_loss = 0
		count = 0
		model.eval()
		for batch in test_loader:
			
			batch_input = batch["original"]
			batch_output = batch["stack"]
			
			batch_input = Variable(batch_input,requires_grad=False, volatile=True).cuda()
			batch_output = Variable(batch_output,requires_grad=False, volatile=True).cuda()
		
			# Forward Pass
			result = model(batch_input)
			MSELoss = loss_fn(result, batch_output)
			#PriorLoss = alpha * focalPenalty(batch_output, result) 
			loss = MSELoss #+ PriorLoss
			
			total_loss += loss.data[0]
			count += 1
			
		test_loss.append(total_loss/count)
		
				
		# Print estimated time of completion
		if epoch==0:
			end_time = time.time()
			num_seconds = end_time-start_time
			estimation = num_seconds*(num_epochs)
			print("\n")
			print("Estimated Time of Completion: " + str(floor(estimation/3600)) + " hours and " + str(floor((estimation % 3600) /60 )) + " minutes")
			print("\n")

			
	###################################Output Saving###############################
	# Make saving directory
	directory = savedir + makeName(topology,b,num_epochs,descriptor)
	ensure_dir(directory)

	# Save the trained model
	saveModel(model, directory)

	# Save loss graphs
	saveLoss(train_loss,test_loss,directory)

	# Save output from all test images
	print("Auto Testing...")
	refocusDirectory(model,imagedir,directory,ImageNet)
	print("Done")