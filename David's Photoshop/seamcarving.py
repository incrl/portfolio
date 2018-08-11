import numpy as np

def grey_scale(image):
    red = image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,2]
    result = 0.299*red + 0.557*green + 0.114*blue
    return result

def convolution(image,kernel):
    
    rows,cols = image.shape
    height, width = kernel.shape
	
    image = image.astype(np.float32)
    result = np.zeros((rows,cols)).astype(np.float32)
    
	#Determine the number of edge pixels
    re = int(height/2)
    ce = int(width/2)
	
    for i in range(0,height):
        for j in range(0,width):
            multiplier = kernel[i,j]
            result[max(0, i-re):rows-re+i,max(0, j-ce):cols-ce+j] += multiplier*image[max(0, re-i):rows+re-i,max(0, ce-j):cols+ce-j]
	
    return result

	
def gaussian_blur(image):
    kernel = np.matrix([[1, 2, 1],
                        [2, 4, 2],
                        [1, 2, 1]])
						
    return (convolution(image,kernel)/16)

def x_gradient(image):
    kernel = np.matrix([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
						
    return (convolution(image,kernel)/8)

def y_gradient(image):
    kernel = np.matrix([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
						
    return (convolution(image,kernel)/8)
	
def get_energy_map(image):
	img_grey = gaussian_blur(grey_scale(image))
	x_grad = x_gradient(img_grey)
	y_grad = y_gradient(img_grey)
	energy_map = np.absolute(x_grad) + np.absolute(y_grad)
	return energy_map
	
def cumulative_vertical_map(energy_map):
	
	out_of_bounds = 1e10
	
	rows, cols = energy_map.shape
	result = np.zeros((rows,cols))
	
	for i in range(1,rows):
		for j in range(0,cols):
			if j == 0:
				left = out_of_bounds
			else:
				left = result[i-1,j-1]
			
			middle = result[i-1,j]
			
			if j == cols-1:
				right = out_of_bounds
			else:
				right = result[i-1,j+1]
			
			result[i,j] = energy_map[i,j] + min(left,middle,right)
			
	return result
	
def cumulative_vertical_map_forward(energy_map):
	
	out_of_bounds = 1e10
	
	rows, cols = energy_map.shape
	result = np.zeros((rows,cols))
	
	for i in range(1,rows):
		for j in range(0,cols):
			if j == 0:
				left = out_of_bounds
			else:
				left = result[i-1,j-1]
			
			middle = result[i-1,j]
			
			if j == cols-1:
				right = out_of_bounds
			else:
				right = result[i-1,j+1]
				
			if j == 0:
				CL = abs(energy_map[i,j+1]) + abs(energy_map[i-1,j])
				CU = abs(energy_map[i,j+1])
				CR = abs(energy_map[i,j+1]) + abs(energy_map[i-1,j] - energy_map[i,j+1])
			elif j == cols-1:
				CL = abs(energy_map[i,j-1]) + abs(energy_map[i-1,j] - energy_map[i,j-1])
				CU = abs(energy_map[i,j-1])
				CR = abs(energy_map[i,j-1]) + abs(energy_map[i-1,j])
			else:
				CL = abs(energy_map[i,j+1] - energy_map[i,j-1]) + abs(energy_map[i-1,j] - energy_map[i,j-1])
				CU = abs(energy_map[i,j+1] - energy_map[i,j-1])
				CR = abs(energy_map[i,j+1] - energy_map[i,j-1]) + abs(energy_map[i-1,j] - energy_map[i,j+1])
			
			result[i,j] = energy_map[i,j] + min(left + CL, middle + CU, right + CR)
			
	return result

def get_min_vertical_seam(vertical_map):
	
	out_of_bounds = 1e10
	
	rows, cols = vertical_map.shape
	indices = []
	
	indices.append(np.argmin(vertical_map[rows-1]))
	
	# Dynamic programming, start at the bottom
	for i in range(1,rows)[::-1]:
		j = indices[-1]
		
		if j == 0:
			left = out_of_bounds
		else:
			left = vertical_map[i-1,j-1]
		
		middle = vertical_map[i-1,j]
		
		if j == cols-1:
			right = out_of_bounds
		else:
			right = vertical_map[i-1,j+1]
		
		# Figure out which direction to step
		next_index = np.argmin([left,middle,right]) - 1
		
		indices.append(j+next_index)
	
	# Switch order so seam goes top to bottom
	indices = indices[::-1]
	
	return indices
	
def draw_vertical_seam(image, vert_seam, color=[0,255,255]):

	# Default Color is Yellow
	result = np.array(image)
	
	for i in range(len(image)):
		seam_index = vert_seam[i]
		result[i,seam_index] = color
		
	return result

def remove_vertical_seam(image, vert_seam):

	rows, cols, ch = image.shape

	# Flatten the image
	flattened = np.reshape(image,(rows*cols,ch))
	
	# Describe the indices in the flattened version of the array
	indices = cols*np.arange(rows)+np.array(vert_seam)

	# Delete those indices from the array
	result = np.delete(flattened, indices, axis=0)
	
	# Reshape the result and return
	return np.reshape(result,(rows,cols-1,ch))
	
def cumulative_horizontal_map(energy_map):

	return cumulative_vertical_map(energy_map.T).T
	
def cumulative_horizontal_map_forward(energy_map):

	return cumulative_vertical_map_forward(energy_map.T).T
	
	
def get_min_horizontal_seam(horizontal_map):
	
	return get_min_vertical_seam(horizontal_map.T)
	
def draw_horizontal_seam(image, horizontal_seam, color=[0,0,255]):
	# Transpose image
	temp = np.transpose(image,axes=(1,0,2))

	# Reuse vertical draw code
	result = draw_vertical_seam(temp,horizontal_seam,color)
	
	# Transpose image back
	return  np.transpose(result,axes=(1,0,2))
	
def remove_horizontal_seam(image, horizontal_seam):

	temp = np.transpose(image,axes=(1,0,2))
	result = remove_vertical_seam(temp,horizontal_seam)
	return  np.transpose(result,axes=(1,0,2))
	