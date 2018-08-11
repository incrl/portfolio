import numpy as np
from matplotlib import colors
import seamcarving as sc
import homography as hm
import transformer_net as tn
import graphcut as gc
import torch
from torch.autograd import Variable

def toHSB(image):
    temp = 255*colors.rgb_to_hsv(image/255.0)
    return temp.astype(np.int32)
    
def toRGB(image):
    temp = 255*colors.hsv_to_rgb(image/255.0)
    return temp.astype(np.int32)

def toGrayScale(image):
    red = image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,2]
    result = 0.299*red + 0.557*green + 0.114*blue
    result = np.expand_dims(result,axis=2)
    image = np.concatenate((result,result,result),axis=2)
    return image.astype(np.uint8)
	
def brightnessAdjust(image, c):
    im = toHSB(image)
    im[:,:,2] = np.maximum(np.minimum(im[:,:,2] + c, 255), 0)
    return toRGB(im).astype(np.uint8)
	
def contrastAdjust(image, c):
    im = toHSB(image)
    im[:,:,2] = ((c + 100.0)/100.0)**4 * (im[:,:,2] - 128.0) + 128.0
    im[:,:,2] = np.maximum(np.minimum(im[:,:,2],255),0)
    return toRGB(im).astype(np.uint8)
	
def medianBlur(image,size=3):
    
    rows,cols,ch = image.shape
    
    result = np.zeros((rows,cols,ch))
    
    #Determine the number of edge pixels to exclude
    re = int(size/2)
    ce = int(size/2)
    
    #Don't include edge cases
    for i in range(re,rows-re): 
        for j in range(ce,cols-ce):
            neighborhood = image[i-re:i+re+1,j-ce:j+ce+1]
			
            # Find the median color
            red = np.median(neighborhood[:,0])
            green = np.median(neighborhood[:,1])
            blue = np.median(neighborhood[:,2])
			
			# Grab the pixel that is closest to the median color
            errors = (red - neighborhood[:,0])**2 + (green - neighborhood[:,1])**2 + (blue - neighborhood[:,2])**2
            index = np.argmin(errors)
            pixel = neighborhood[index//size,index%size]

            # Set new color to that pixel
            result[i,j] = pixel
    
    return result.astype(np.uint8)
	
def convolution(image,kernel):
    
    rows,cols,ch = image.shape
    height, width = kernel.shape
	
    image = image.astype(np.float32)
    result = np.zeros((rows,cols,ch)).astype(np.float32)
    
	#Determine the number of edge pixels
    re = int(height/2)
    ce = int(width/2)
	
    for i in range(0,height):
        for j in range(0,width):
            multiplier = kernel[i,j]
            result[max(0, i-re):rows-re+i,max(0, j-ce):cols-ce+j] += multiplier*image[max(0, re-i):rows+re-i,max(0, ce-j):cols+ce-j]
	
    #Slow convolution
    #for i in range(re,rows-re): 
        #for j in range(ce,cols-ce):
            #neighborhood = image[i-re:i+re+1,j-ce:j+ce+1]
            #red = np.sum(np.multiply(kernel,neighborhood[:,:,0]))
            #green = np.sum(np.multiply(kernel,neighborhood[:,:,1]))
            #blue = np.sum(np.multiply(kernel,neighborhood[:,:,2]))
            #result[i,j] = [red,green,blue]
	
    return result

def averageBlur(image):
    
    kernel = np.matrix([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])
    
    return (convolution(image,kernel)/9).astype(np.uint8)

def sharpen(image):
    
    kernel = np.matrix([[0, -1, 0],
                        [-1, 6, -1],
                        [0, -1, 0]])
    
    return (convolution(image,kernel)/2).astype(np.uint8)
	
def edgeDetect(image):
    
    image = toGrayScale(image)
	
    kernelx = np.matrix([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    xvals = convolution(image,kernelx) 
    
    kernely = np.matrix([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    
    yvals = convolution(image,kernely) 
    
    result = np.sqrt(xvals**2 + yvals**2)
	
    return result.astype(np.uint8)
	
def seamCarve(img, dx, dy):
	
	images = []
	
	for _ in range(dx):
		energy_map = sc.get_energy_map(img)
		vmap = sc.cumulative_vertical_map(energy_map)
		vseam = sc.get_min_vertical_seam(vmap)
		img = sc.draw_vertical_seam(img,vseam)
		images.append(img)
		img = sc.remove_vertical_seam(img,vseam)
		images.append(img)
		
	for _ in range(dy):
		energy_map = sc.get_energy_map(img)
		hmap = sc.cumulative_horizontal_map(energy_map)
		hseam = sc.get_min_horizontal_seam(hmap)
		img = sc.draw_horizontal_seam(img,hseam)
		images.append(img)
		img = sc.remove_horizontal_seam(img,hseam)
		images.append(img)

	return img,images
	
def seamCarveX(img,forwardEnergy = True):
    energy_map = sc.get_energy_map(img)
    if forwardEnergy:
        vmap = sc.cumulative_vertical_map_forward(energy_map)
    else:
        vmap = sc.cumulative_vertical_map(energy_map)
    vseam = sc.get_min_vertical_seam(vmap)
    marked = sc.draw_vertical_seam(img,vseam)
    img = sc.remove_vertical_seam(img,vseam)
    return img, marked
	
def seamCarveY(img,forwardEnergy = True):
    energy_map = sc.get_energy_map(img)
    if forwardEnergy:
        hmap = sc.cumulative_horizontal_map_forward(energy_map)
    else:
        hmap = sc.cumulative_horizontal_map(energy_map)
    hseam = sc.get_min_horizontal_seam(hmap)
    marked = sc.draw_horizontal_seam(img,hseam)
    img = sc.remove_horizontal_seam(img,hseam)
    return img, marked

def performHomography(source,t0,t1,t2,t3):
    
    rows,cols,ch = source.shape
    target = np.zeros((rows,cols,ch))

	# Define 8 points system
    s0 = hm.Point(0,0)
    s1 = hm.Point(cols,0)
    s2 = hm.Point(cols,rows)
    s3 = hm.Point(0,rows)
    t0 = hm.Point(t0[1],t0[0])
    t1 = hm.Point(t1[1],t1[0])
    t2 = hm.Point(t2[1],t2[0])
    t3 = hm.Point(t3[1],t3[0])
	
    transform = hm.getHomography(s0,s1,s2,s3,t0,t1,t2,t3)
    invHomography = np.linalg.inv(transform)

    xvals, yvals = hm.getCanvas(t0,t1,t2,t3)   
    
    for xc in xvals:
        for yc in yvals:
            h_pt = np.matrix([[xc],[yc],[1]])
            c_pt = invHomography*h_pt
            x = c_pt[0]/c_pt[2]
            y = c_pt[1]/c_pt[2]

            target[yc,xc] = hm.interpolate(source,x,y) 
    
    return target.astype(np.uint8)

def graphCut(img, foreground, background, grayscale = True ,sigma = .1):
    
    img = img.astype(np.float32)
    fg, bg = gc.getTEdges(img, foreground, background, sigma)
    g, nodeids = gc.getGraph(img, fg, bg, sigma)
    return gc.cutAndPlot(g, nodeids, img, grayscale).astype(np.uint8)
	
def styleTransfer(image, model_fn):

	style_model = tn.TransformerNet()
	style_model.load_state_dict(torch.load(model_fn))

	if torch.cuda.is_available():
		style_model.cuda()

	content_image = np.array(image).transpose(2, 0, 1)
	content_image = torch.from_numpy(content_image).float()
	content_image = content_image.unsqueeze(0)

	if torch.cuda.is_available():
		content_image = content_image.cuda()
		
	# Preprocess Image
	content_image = content_image.transpose(0, 1)
	(r, g, b) = torch.chunk(content_image, 3)
	content_image = torch.cat((b, g, r))
	content_image = content_image.transpose(0, 1)
		
	# Style Transfer
	content_image = Variable(content_image, volatile=True)		
	output = style_model(content_image)

	# Return image
	(b, g, r) = torch.chunk(output.data[0], 3)
	output = torch.cat((r, g, b))

	if torch.cuda.is_available():
		img = output.clone().cpu().clamp(0, 255).numpy()
	else:
		img = output.clone().clamp(0, 255).numpy()
	img = img.transpose(1, 2, 0).astype('uint8')

	return img
    
