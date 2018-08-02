import torch.nn as nn
import torch.nn.functional as F
import torch
import torchvision
from torch import cat, FloatTensor
from torch.autograd import Variable

class SimpleModel(nn.Module):
	def __init__(self):
		super(SimpleModel, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, 3, stride=1, padding=1)
		self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.conv3 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.conv4 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.conv5 = nn.Conv2d(64, 32, 3, stride=1, padding=1)
		self.conv6 = nn.Conv2d(32, 16, 3, stride=1, padding=1)
		self.conv7 = nn.Conv2d(16, 15, 3, stride=1, padding=1)

	def forward(self, x):
		x = F.relu(self.conv1(x))
		x = F.relu(self.conv2(x))
		x = F.relu(self.conv3(x))
		x = F.relu(self.conv4(x))
		x = F.relu(self.conv5(x))
		x = F.relu(self.conv6(x))
		result = F.sigmoid(self.conv7(x))

		# Reshape appropriately
		_,ch,rows,cols = result.size()
		result = result.view(-1,ch//3,3,rows,cols)
		return result
		
		
class SimpleUnet(nn.Module):

	def UnetPad(self, in_img):
	
		_,_,h,w = in_img.size()
		
		h_pad = (16 - h % 16) % 16
		w_pad = (16 - w % 16) % 16

		pad = nn.modules.padding.ZeroPad2d((0,w_pad,0,h_pad))
		
		result = pad(in_img)
		
		return result

	def __init__(self):
		super(SimpleUnet, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, 3, stride=1, padding=1)
		self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv3 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
		self.conv4 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
		self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv5 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
		self.conv6 = nn.Conv2d(256, 256, 3, stride=1, padding=1)
		self.upconv1 =  nn.ConvTranspose2d(256,128,kernel_size=2,stride=2)
		self.conv7 = nn.Conv2d(256, 128, 3, stride=1, padding=1)
		self.conv8 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
		self.upconv2 =  nn.ConvTranspose2d(128,64,kernel_size=2,stride=2)
		self.conv9 = nn.Conv2d(128, 64, 3, stride=1, padding=1)
		self.conv10 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.final = nn.Conv2d(64, 15, 1, stride=1, padding=0)

	def forward(self, x):
	
		# Pad the input appropriately
		_, _, start_rows, start_cols = x.size()
		x = self.UnetPad(x)
	
		x = F.relu(self.conv1(x))
		saved1 = F.relu(self.conv2(x))
		x = self.pool1(saved1)
		x = F.relu(self.conv3(x))
		saved2 = F.relu(self.conv4(x))
		x = self.pool2(saved2)
		x = F.relu(self.conv5(x))
		x = F.relu(self.conv6(x))
		x = self.upconv1(x)
		x = cat((x, saved2), 1)
		x = F.relu(self.conv7(x))
		x = F.relu(self.conv8(x))
		x = self.upconv2(x)
		x = cat((x,saved1), 1)
		x = F.relu(self.conv9(x))
		x = F.relu(self.conv10(x))
		result = F.sigmoid(self.final(x))

		# Reshape appropriately
		_,ch,rows,cols = result.size()
		result = result.view(-1,ch//3,3,rows,cols)
		
		# Unpad
		result = result[:,:,:,:start_rows,:start_cols]
		
		return result
	
	
class Unet3D(nn.Module):

	def UnetPad(self, in_img):
	
		_,_,h,w = in_img.size()
		
		h_pad = (16 - h % 16) % 16
		w_pad = (16 - w % 16) % 16

		pad = nn.modules.padding.ZeroPad2d((0,w_pad,0,h_pad))
		
		result = pad(in_img)
		
		return result

	def __init__(self):
		super(Unet3D, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, 3, stride=1, padding=1)
		self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv3 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
		self.conv4 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
		self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv5 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
		self.conv6 = nn.Conv3d(256, 256, 3, stride=1, padding=1)
		self.upconv1 =  nn.ConvTranspose3d(256,128,kernel_size=(1,2,2),stride=(1,2,2))
		self.conv7 = nn.Conv3d(256, 128, 3, stride=1, padding=1)
		self.conv8 = nn.Conv3d(128, 128, 3, stride=1, padding=1)
		self.upconv2 =  nn.ConvTranspose3d(128,64,kernel_size=(1,2,2),stride=(1,2,2))
		self.conv9 = nn.Conv3d(128, 64, 3, stride=1, padding=1)
		self.conv10 = nn.Conv3d(64, 64, 3, stride=1, padding=1)
		self.final = nn.Conv3d(64, 3, 1, stride=1, padding=0)

	def forward(self, x):
	
		# Pad the input appropriately
		_, _, start_rows, start_cols = x.size()
		x = self.UnetPad(x)
	
		x = F.relu(self.conv1(x))
		s1 = F.relu(self.conv2(x))
		x = self.pool1(s1)
		x = F.relu(self.conv3(x))
		s2 = F.relu(self.conv4(x))
		x = self.pool2(s2)
		x = F.relu(self.conv5(x))
		
		# Switch to 3D inputs by copying current information to each frame
		x = x[:,:,None] # Add dimension
		x = cat((x,x,x,x,x),2)
		
		x = F.relu(self.conv6(x))
		x = self.upconv1(x)
		s2 = s2[:,:,None]
		s2 = cat((s2,s2,s2,s2,s2),2)
		x = cat((x, s2), 1)
		x = F.relu(self.conv7(x))
		x = F.relu(self.conv8(x))
		x = self.upconv2(x)
		s1 = s1[:,:,None]
		s1 = cat((s1,s1,s1,s1,s1),2)
		x = cat((x,s1), 1)
		x = F.relu(self.conv9(x))
		x = F.relu(self.conv10(x))
		result = F.sigmoid(self.final(x))
		
		# Rearrange Output
		result = result.permute(0,2,1,3,4)
		
		# Unpad
		result = result[:,:,:,:start_rows,:start_cols]
		
		return result
		
class EncodeDecode3D(nn.Module):

	def UnetPad(self, in_img):
	
		_,_,h,w = in_img.size()
		
		h_pad = (16 - h % 16) % 16
		w_pad = (16 - w % 16) % 16

		pad = nn.modules.padding.ZeroPad2d((0,w_pad,0,h_pad))
		
		result = pad(in_img)
		
		return result

	def __init__(self):
		super(EncodeDecode3D, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, 3, stride=1, padding=1)
		self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv3 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
		self.conv4 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
		self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv5 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
		self.conv6 = nn.Conv3d(256, 256, 3, stride=1, padding=1)
		self.upconv1 =  nn.ConvTranspose3d(256,128,kernel_size=(1,2,2),stride=(1,2,2))
		self.conv7 = nn.Conv3d(128, 128, 3, stride=1, padding=1)
		self.conv8 = nn.Conv3d(128, 128, 3, stride=1, padding=1)
		self.upconv2 =  nn.ConvTranspose3d(128,64,kernel_size=(1,2,2),stride=(1,2,2))
		self.conv9 = nn.Conv3d(64, 64, 3, stride=1, padding=1)
		self.conv10 = nn.Conv3d(64, 64, 3, stride=1, padding=1)
		self.final = nn.Conv3d(64, 3, 1, stride=1, padding=0)

	def forward(self, x):
	
		# Pad the input appropriately
		_, _, start_rows, start_cols = x.size()
		x = self.UnetPad(x)
	
		x = F.relu(self.conv1(x))
		x = F.relu(self.conv2(x))
		x = self.pool1(x)
		x = F.relu(self.conv3(x))
		x = F.relu(self.conv4(x))
		x = self.pool2(x)
		x = F.relu(self.conv5(x))
		
		# Switch to 3D inputs by copying current information to each frame
		x = x[:,:,None] # Add dimension
		x = cat((x,x,x,x,x),2)
		
		x = F.relu(self.conv6(x))
		x = self.upconv1(x)
		x = F.relu(self.conv7(x))
		x = F.relu(self.conv8(x))
		x = self.upconv2(x)
		x = F.relu(self.conv9(x))
		x = F.relu(self.conv10(x))
		result = F.sigmoid(self.final(x))
		
		# Rearrange Output
		result = result.permute(0,2,1,3,4)
		
		# Unpad
		result = result[:,:,:,:start_rows,:start_cols]
		
		return result

class ConditionalInstanceNorm(nn.Module):

	def UnetPad(self, in_img):
	
		_,_,h,w = in_img.size()
		
		h_pad = (16 - h % 16) % 16
		w_pad = (16 - w % 16) % 16

		pad = nn.modules.padding.ZeroPad2d((0,w_pad,0,h_pad))
		
		result = pad(in_img)
		
		return result
		
	def CIN(self, x, encoding):
		x = x + torch.mean(x,1,keepdim=True)
		x = x/torch.std(x,1,keepdim=True)
		gamma = torch.sum(torch.mul(encoding,self.scales))
		beta = torch.sum(torch.mul(encoding,self.biases))
		
		return gamma*x + beta

	def __init__(self):
		super(ConditionalInstanceNorm, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, 3, stride=1, padding=1)
		self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv3 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
		self.conv4 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
		self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
		self.conv5 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
		self.conv6 = nn.Conv2d(256, 256, 3, stride=1, padding=1)
		self.upconv1 =  nn.ConvTranspose2d(256,128,kernel_size=2,stride=2)
		self.conv7 = nn.Conv2d(256, 128, 3, stride=1, padding=1)
		self.conv8 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
		self.upconv2 =  nn.ConvTranspose2d(128,64,kernel_size=2,stride=2)
		self.conv9 = nn.Conv2d(128, 64, 3, stride=1, padding=1)
		self.conv10 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
		self.final = nn.Conv2d(64, 3, 1, stride=1, padding=0)
		
		self.scales = nn.Parameter(FloatTensor([1,1,1,1,1]))
		self.biases = nn.Parameter(FloatTensor([0,0,0,0,0]))

	def forward(self, x, encoding = None):
	
		if encoding == None:
			encoding = FloatTensor([0,0,1,0,0])
		else:
			encoding = FloatTensor(encoding)
	
		# Pad the input appropriately
		_, _, start_rows, start_cols = x.size()
		start = self.UnetPad(x)
	
		x = F.relu(self.conv1(start))
		saved1 = F.relu(self.conv2(x))
		x = self.pool1(saved1)
		x = F.relu(self.conv3(x))
		saved2 = F.relu(self.conv4(x))
		x = self.pool2(saved2)
		features = F.relu(self.conv5(x))
		
		# Perform Conditional Instance Normalization
		result = start[:,None]
		encoding = Variable(encoding,requires_grad=False).cuda()
		x = self.CIN(features,encoding)
		x = F.relu(self.conv6(x))
		x = self.upconv1(x)
		x = self.CIN(x,encoding)
		x = cat((x, saved2), 1)
		x = F.relu(self.conv7(x))
		x = self.CIN(x,encoding)
		x = F.relu(self.conv8(x))
		x = self.upconv2(x)
		x = self.CIN(x,encoding)
		x = cat((x,saved1), 1)
		x = F.relu(self.conv9(x))
		x = self.CIN(x,encoding)
		x = F.relu(self.conv10(x))
		x = F.sigmoid(self.final(x))
		x = x[:,None]

		
		# Unpad and remove starting result
		result = x[:,:,:,:start_rows,:start_cols]
		
		#print(self.scales)
		#print(self.biases)
		#print(result.size())
		
		return result

		
class myResNet18(nn.Module):

	def __init__(self):
		super(myResNet18, self).__init__()

		self.resnet = torchvision.models.resnet18(pretrained = True)

		self.decoder = nn.Sequential(
			nn.ConvTranspose2d(512,256,kernel_size=2,stride=2),
			nn.ConvTranspose2d(256,128,kernel_size=2,stride=2),
			nn.ConvTranspose2d(128,64,kernel_size=2,stride=2),
			nn.ConvTranspose2d(64,32,kernel_size=2,stride=2),
			nn.ConvTranspose2d(32,15,kernel_size=2,stride=2)
			)

	def forward(self, x):
		x = self.resnet.conv1(x)
		x = self.resnet.bn1(x)
		x = self.resnet.relu(x)
		x = self.resnet.maxpool(x)
		x=self.resnet.layer1(x)
		x=self.resnet.layer2(x)
		x=self.resnet.layer3(x)
		x=self.resnet.layer4(x)
		x = self.decoder(x)
		_,ch,rows,cols = x.size()
		x = x.view(-1,ch//3,3,rows,cols)

		return x


		

