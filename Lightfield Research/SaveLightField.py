import numpy as np
from tqdm import tqdm
from scipy.misc import imresize, imsave

def saveImage(im, filename):
	imsave(filename,im)

def saveGantry(lf, directory):
	count=0
	for r in lf:
		for c in r:
			saveImage(c,directory+"{:3d}".format(count)+".png")
			count+=1
	
def saveFocalStack(stack, foci, filename, filetype=".png"):
	
	for i in range(len(stack)):
		imsave(filename + "_" + str(foci[i]) + "_" + filetype, stack[i])
		
def saveGIF(images, filename="output.gif"):
	import imageio
	imageio.mimsave(filename, images, fps=5)

# Note: To use this function,  you may need to install the ffmpeg codec to your computer.
def saveMP4(images, filename="output.mp4"):
	print("Saving...")
		
	import matplotlib.animation as animation
	import matplotlib.pyplot as plt
	mp4Writer = animation.writers['ffmpeg']
	the_writer = mp4Writer(fps=15, metadata=dict(artist='Me'))
	fig = plt.figure()
	ims = []
	
	rows, cols, _ = images[0].shape
	
	#plt.axis([0, cols, rows, 0])
	plt.axis('off')
	
	for image in images:
		ims.append([plt.imshow(image,vmin=0,vmax=255,animated=True)])
		
	im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)
	im_ani.save(filename, writer=the_writer)
	print("Done")
	
def saveNPY(lf, filename):
	return np.save(filename, lf)