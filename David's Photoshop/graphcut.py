import maxflow
import numpy as np
from matplotlib import colors

# Make a color distance function
def dist(rgb1, rgb2):
    return (rgb1[0]-rgb2[0])**2 + (rgb1[1]-rgb2[1])**2 + (rgb1[2]-rgb2[2])**2
	
def distNP(img, rgb):
    return (img[:,:,0]-rgb[0])**2 + (img[:,:,1]-rgb[1])**2 + (img[:,:,2]-rgb[2])**2
	
def getTEdges(img, foreground, background, sigma = .1):

    (rows, cols, ch) = img.shape

    # Determine Source and Terminal Edges
    bg_results = np.zeros((rows,cols))
    fg_results = np.zeros((rows,cols))

    total = np.zeros((rows,cols))

	# Background comparison
    for bg_loc in background:

        rgb_bg = img[bg_loc[0],bg_loc[1]]

		#Gaussian Weighting Function
        total += np.exp(-distNP(img,rgb_bg)/(sigma))
		
    bg_results = total/len(background)
	
	
    total = np.zeros((rows,cols))
	
	# Foreground comparison
    for fg_loc in foreground:

        rgb_fg = img[fg_loc[0],fg_loc[1]]

		#Gaussian Weighting Function
        total += np.exp(-distNP(img,rgb_fg)/(sigma))

    fg_results = total/len(foreground)
            
    return fg_results, bg_results
	
def getGraph(img, fg_results, bg_results, sigma = .1):

    (rows, cols, ch) = img.shape
    
    # Generate Max Flow Graph
    g = maxflow.Graph[float]()
    nodeids = g.add_grid_nodes((rows,cols))

    # Add Source and Terminal Weights
    g.add_grid_tedges(nodeids, fg_results, bg_results)

    # Get Neighbor Weights
    for i in range(0, rows-1):
        for j in range(0, cols-1):

            val_right = np.exp(-dist(img[i][j],img[i][j+1])/(sigma))
            val_down  = np.exp(-dist(img[i][j],img[i+1][j])/(sigma))

            g.add_edge(nodeids[i][j], nodeids[i][j+1], val_right, val_right)
            g.add_edge(nodeids[i][j], nodeids[i+1][j], val_down, val_down)

    # Right and Bottom Edge
    for i in range(0, rows-1):
        val_down = np.exp(-dist(img[i][cols-1],img[i+1][cols-1])/(2*sigma))
        g.add_edge(nodeids[i][j], nodeids[i+1][j], val_down, val_down)

    for j in range(0, cols-1):
        val_right = np.exp(-dist(img[rows-1][j],img[rows-1][j+1])/(2*sigma))
        g.add_edge(nodeids[rows-1][j], nodeids[rows-1][j+1], val_right, val_right)
        
    return g, nodeids
	
def cutAndPlot(g, nodeids,img, grayscale=True):
    # Grab Foreground and Background
    g.maxflow()

    sgm = g.get_grid_segments(nodeids)

    answer = np.int_(np.logical_not(sgm))
    
    #print(answer)
	
    # Plot Original Image with Grey Scale selection
    if grayscale:
    
        (rows, cols, ch) = img.shape
    
        hsv = colors.rgb_to_hsv(img)

        for i in range(0,rows):
            for j in range(0,cols):

                #Grey out background
                hsv[i,j,1] = hsv[i,j,1] * answer[i][j]

        final = colors.hsv_to_rgb(hsv)
		
        return final
	
    else:	
        return answer