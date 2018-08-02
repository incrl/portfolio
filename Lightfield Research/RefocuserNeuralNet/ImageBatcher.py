import numpy as np
from tqdm import tqdm
from LoadLightField import *
from LightFieldFunctions import *
from SaveLightField import *
import os

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
	
    return file_path
	
loadDirectories =  ["D:\\LightFieldData\\ESPL\\4D_LF\\Buildings\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Grids\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\ISO_and_Colour_Charts\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Landscapes\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Light\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Mirrors_and_Transparency\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Nature\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\People\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Studio\\",
					"D:\\LightFieldData\\ESPL\\4D_LF\\Urban\\"]
					
metaDirectories = [None,
				   None,
				   None,
				   None,
				   None,
				   None,
				   None,
				   None,
				   None,
				   None]

saveDirectories = ["D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\",
				   "D:\\LightFieldData\\Focal2\\"]

loadDirectories = ["D:\\LightFieldData\\Stanford\\bikes\\raw\\",
				   "D:\\LightFieldData\\Stanford\\buildings\\raw\\",
				   "D:\\LightFieldData\\Stanford\\cars\\raw\\",
				   "D:\\LightFieldData\\Stanford\\flowers_plants\\raw\\",
				   "D:\\LightFieldData\\Stanford\\fruits_vegetables\\raw\\",
				   "D:\\LightFieldData\\Stanford\\general\\raw\\",
				   "D:\\LightFieldData\\Stanford\\occlusions\\raw\\",
				   "D:\\LightFieldData\\Stanford\\people\\raw\\",
				   "D:\\LightFieldData\\Stanford\\reflective\\raw\\"]


metaDirectories = ["D:\\LightFieldData\\Stanford\\bikes\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\buildings\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\cars\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\flowers_plants\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\fruits_vegetables\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\general\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\occlusions\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\people\\metadata\\",
				   "D:\\LightFieldData\\Stanford\\reflective\\metadata\\"]

saveDirectories = ["D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\",
				   "D:\\LightFieldData\\Focal\\"]
				   


				   
# Refocus parameters
#alphas = [.5,.6,.7,.8,.9,1.0,1.2,1.4,1.6,1.8,2.0]
#alphas = [1.0]
#alphas = [.5,.6,.7,.8,.9,1.0,1.0/.9,1.0/.8,1.0/.7,1.0/.6,1.0/.5]
alphas = [.9**5,.9**4,.9**3,.9**2,.9,1,1/(.9),1/(.9**2),1/(.9**3),1/(.9**4),1/(.9**5)]

for i in range(len(loadDirectories)):
	
	loaddir = loadDirectories[i]
	metadir = metaDirectories[i]
	savedir = saveDirectories[i]

	for f in tqdm(os.listdir(loaddir)):
		
		# Determine File Type
		name,extension = f.split(".")
		
		# Load light field
		if extension == "png":
			#Strip _eslf off filename
			name = name[:-5]
			lf = loadESLF(loaddir + f, metadir + name + ".json")
			
		elif extension == "mat":
			lf = loadMAT(loaddir + f)
		else:
			continue
		
		# Refocus for each alpha in the focal stack and repeat
		for alpha in alphas:
			refocused = refocus(lf, alpha)
			saveImage(refocused, ensure_dir(savedir + "refocused_"+ "{:.4f}".format(alpha)+ "\\" + name + "_0.png"))

			# Augment Data and Repeat
			#refocused = refocused[::-1]
			#saveImage(refocused, savedir + "refocused_"+ str(alpha)+ "\\" + name + "_1.png")

			#refocused = refocused[:,::-1]
			#saveImage(refocused, savedir + "refocused_"+ str(alpha)+ "\\" + name + "_2.png")
			
			#refocused = refocused[::-1]
			#saveImage(refocused, savedir + "refocused_"+ str(alpha)+ "\\" + name + "_3.png")
			
