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


####################################Setting Parameters##################################
# topology = Topology of the network to train with
# split = Train/Test split (i.e. the number of images to include in the training set)

topology = 5
learning_rate = 1e-4
b = 1 # Number of images per round
skip = 2 # Number of iterations before a print
num_epochs = 100
alpha = 1e-4

train_directory = "C:\\Users\\david\\Documents\\FocalNPY\\ConvergenceTest"
test_directory = "C:\\Users\\david\\Documents\\FocalNPY\\ConvergenceTest"
#train_directory = "C:\\Users\\david\\Documents\\FocalNPY\\Train"
#test_directory = "C:\\Users\\david\\Documents\\FocalNPY\\Test"

savedir = "D:\\Refocuser\\Results\\"
imagedir = "images\\"
descriptor = "testing"

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

	def __init__(self, root_dir, stack_size=5, reflections=False):

		self.root_dir = root_dir
		self.files = os.listdir(root_dir)
		self.num_files = len(self.files)
		self.stack_size=stack_size
		self.reflections = reflections
		
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
		
		# Load the data
		sample = {'original': torch.from_numpy(original), 'stack': torch.from_numpy(stack)}

		return sample

# Setup Dataloaders
train_data = FocalStackDataset(train_directory)
train_loader = DataLoader(train_data, batch_size=b, shuffle=True)
test_data = FocalStackDataset(test_directory)
test_loader = DataLoader(test_data, batch_size=b, shuffle=True)


###########################################Model Training#########################################

	
if topology == 5:
	model = ConditionalInstanceNorm() 
	
model.cuda()
	
loss_fn = torch.nn.MSELoss(size_average=True)
params = model.parameters()
optimizer = torch.optim.Adam(params, lr=learning_rate)

train_loss = []
test_loss = []

for epoch in range(num_epochs):

	if epoch == 0:
			start_time = time.time()

	print("Epoch", epoch)
	i = 0

	model.train()
	for batch in train_loader:
		
		batch_input = batch["original"]
		batch_output = batch["stack"]
		
		batch_input = Variable(batch_input,requires_grad=False).cuda()
		batch_output = Variable(batch_output,requires_grad=False).cuda()
	
		losslist = []
	
		# Forward Pass for each view
		result = model(batch_input, [1,0,0,0,0])
		MSELoss = loss_fn(result, batch_output[:,[0]])
		loss = MSELoss
		losslist.append(MSELoss.data[0])
		
		# Training step
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		
		result = model(batch_input, [0,1,0,0,0]);MSELoss = loss_fn(result, batch_output[:,[1]]);loss = MSELoss;losslist.append(MSELoss.data[0])
		optimizer.zero_grad();loss.backward();optimizer.step()
		
		result = model(batch_input, [0,0,1,0,0]);MSELoss = loss_fn(result, batch_output[:,[2]]);loss = MSELoss;losslist.append(MSELoss.data[0])
		optimizer.zero_grad();loss.backward();optimizer.step()
	
		result = model(batch_input, [0,0,0,1,0]);MSELoss = loss_fn(result, batch_output[:,[3]]);loss = MSELoss;losslist.append(MSELoss.data[0])
		optimizer.zero_grad();loss.backward();optimizer.step()
	
		result = model(batch_input, [0,0,0,0,1]);MSELoss = loss_fn(result, batch_output[:,[4]]);loss = MSELoss;losslist.append(MSELoss.data[0])
		optimizer.zero_grad();loss.backward();optimizer.step()
	
		# Printing statement
		i += 1
		if i % skip == 0:
			print(i,losslist[0],losslist[1],losslist[2],losslist[3],losslist[4])
			train_loss.append(sum(losslist))
		
	
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
		result1 = model(batch_input, [1,0,0,0,0])
		result2 = model(batch_input, [0,1,0,0,0])
		result3 = model(batch_input, [0,0,1,0,0])
		result4 = model(batch_input, [0,0,0,1,0])
		result5 = model(batch_input, [0,0,0,0,1])
		result = cat((result1,result2,result3,result4,result5),1)
		MSELoss = loss_fn(result, batch_output) 
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
refocusDirectory2(model,imagedir,directory)
print("Done")