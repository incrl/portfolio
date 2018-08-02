import os
import numpy as np
from scipy.misc import imsave
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import torch

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def makeName(topology, split, b, descriptor=""):
	if topology == 1:
		text = "CNN"
	if topology == 2:
		text = "Unet"
	if topology == 3:
		text = "CNNwithBatchNorm"
	return text + "Split" + str(split) + "Batch" + str(b) + descriptor + "\\"

def saveModel(model, directory="", fn="trained_model.pt"):
	torch.save(model, directory+fn)
	
def saveImages(original, refocused, learned_images, directory=""):
	# Rearrange back into regular image format
	original = np.transpose(original,(0,2,3,1))
	refocused = np.transpose(refocused,(0,2,3,1))

	# Save the original and refocused images
	imsave(directory + "original.png", original[0])
	imsave(directory + "refocused.png", refocused[0])

	# Save final learned result
	learned_image = learned_images[-1]
	learned_image = np.transpose(learned_image,(0,2,3,1))
	imsave(directory + "learned.png", learned_image[0])

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
	
def saveLoss(tot_loss_vals,mse_loss_vals=None,res_loss_vals=None,directory=""):
	np.save(directory+"total_loss",np.array(tot_loss_vals))
	fig, ax = plt.subplots(1, 1)
	plt.plot(tot_loss_vals)
	plt.savefig(directory+"total_loss.png", dpi=960, bbox_inches="tight")
	
	if mse_loss_vals:
		np.save(directory+"mean_square_loss",np.array(mse_loss_vals))
		fig, ax = plt.subplots(1, 1)
		plt.plot(mse_loss_vals)
		plt.savefig(directory+"mean_square_loss.png", dpi=960, bbox_inches="tight")
	
	if res_loss_vals:
		np.save(directory+"residual_loss",np.array(res_loss_vals))
		fig, ax = plt.subplots(1, 1)
		plt.plot(res_loss_vals)
		plt.savefig(directory+"residual_loss.png", dpi=960, bbox_inches="tight")
	
def saveLog(topology, split, learning_rate, batch_size, use_whitening, num_epochs, use_residual, use_delay, sub_epochs, res_factor, directory="", fn="parameters.txt"):
	with open(directory+fn, "w") as f:
		if topology == 1:
			text = "CNN"
		if topology == 2:
			text = "Unet"
		if topology == 3:
			text = "CNNwithBatchNorm"
		f.write("Topology: " + text + "\n")
		f.write("Split: " + str(split) + "\n")
		f.write("Learning Rate: " + str(learning_rate) + "\n")
		f.write("Batch Size: " + str(batch_size) + "\n")
		f.write("Used Whitening: " + str(use_whitening) + "\n")
		f.write("Number of Epochs: " + str(num_epochs) + "\n")
		f.write("Used Residual: " + str(use_residual) + "\n")
		f.write("Used Delayed Penalty: " + str(use_delay) + "\n")
		if use_delay:
			f.write("Number of Penalty Epochs: " + str(sub_epochs) + "\n")
			f.write("Residual Factor: " + str(res_factor) + "\n")
			