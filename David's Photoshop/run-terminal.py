from photoshop import *
import cv2
import sys
from time import sleep

cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
filename = sys.argv[1]
image = cv2.imread(filename)
cv2.imshow('Image', image)
cv2.waitKey(1)

print("Functions")
print("-1. Exit")
print("0. Reload Image")
print("1. To Grayscale")
print("2. Brightness Adjustment")
print("3. Contrast Adjustment")
print("4. Median Blur")
print("5. Average Blur")
print("6. Sharpen")
print("7. Edge Detect")
print("8. Seam Carving")
print("9. Homography")
print("10. Graph Cut")
print("11. Van Gogh")
print("12. Candy")
print("13. Mosaic")
print("14. Udnie")
print("15. Save Image")

while(True):

	num = int(input("Which function?:"))
	if num == -1:
		break
	elif num == 0:
		image = cv2.imread(filename)
	elif num == 1:
		image = toGrayScale(image[:,:,::-1])
	elif num == 2:
		c = int(input("How much?:"))
		image = brightnessAdjust(image[:,:,::-1],c)[:,:,::-1]
	elif num == 3:
		c = int(input("How much?:"))
		image = contrastAdjust(image[:,:,::-1],c)[:,:,::-1]
	elif num == 4:
		image = medianBlur(image)
	elif num == 5:
		image = averageBlur(image)
	elif num == 6:
		image = sharpen(image)
	elif num == 7:
		image = edgeDetect(image)
	elif num == 8:
		dx = int(input("How much x?:"))
		dy = int(input("How much y?:"))
		choice = input("Forward Energy? (Y/N):")
		if choice == "Y" or choice == "y" or choice == "yes":
			forwardEnergy = True
		else:
			forwardEnergy = False
		for _ in range(dx):
			image, marked = seamCarveX(image[:,:,::-1],forwardEnergy)
			image = image[:,:,::-1]
			marked = marked[:,:,::-1]
			cv2.imshow("Image",marked)
			cv2.waitKey(1)
			sleep(.25)
			cv2.imshow("Image",image)
			cv2.waitKey(1)
		for _ in range(dy):
			image, marked = seamCarveY(image[:,:,::-1],forwardEnergy)
			image = image[:,:,::-1]
			marked = marked[:,:,::-1]
			cv2.imshow("Image",marked)
			cv2.waitKey(1)
			sleep(.25)
			cv2.imshow("Image",image)
			cv2.waitKey(1)
		#image,images = seamCarve(image[:,:,::-1],dx,dy)
		#image=image[:,:,::-1]
		#for im in images:
			#cv2.imshow("Image",im[:,:,::-1])
			#cv2.waitKey(1)
			#sleep(.25)
	elif num == 9:
		choice = input("Use Defaults? (Y/N):")
		if choice == "Y" or choice == "y" or choice == "yes":
			rows,cols,_ = image.shape
			t0 = (int(.1*rows), int(.2*cols))
			t1 = (int(.05*rows), int(.9*cols))
			t2 = (int(.9*rows), int(.8*cols))
			t3 = (int(.8*rows), int(.1*cols))
			image = performHomography(image,t0,t1,t2,t3)
		else:
			print(image.shape)
			t0 = input("Top Left?:")
			t1 = input("Top Right?:")
			t2 = input("Bottom Right?:")
			t3 = input("Bottom Left?:")
			t0 = (int(t0.split(" ")[0]),int(t0.split(" ")[1]))
			t1 = (int(t1.split(" ")[0]),int(t1.split(" ")[1]))
			t2 = (int(t2.split(" ")[0]),int(t2.split(" ")[1]))
			t3 = (int(t3.split(" ")[0]),int(t3.split(" ")[1]))
			image = performHomography(image,t0,t1,t2,t3)
	elif num == 10:
		fg = input("Foreground Coordinate?:")
		bg = input("Background Coordinate?:")
		fg = [[int(fg.split(" ")[0]),int(fg.split(" ")[1])]]
		bg = [[int(bg.split(" ")[0]),int(bg.split(" ")[1])]]
		image = graphCut(image, fg, bg, grayscale = True ,sigma = .1)
	elif num == 11:
		image = styleTransfer(image[:,:,::-1],"Models/starry-night.pth")[:,:,::-1]
	elif num == 12:
		image = styleTransfer(image[:,:,::-1],"Models/candy.pth")[:,:,::-1]
	elif num == 13:
		image = styleTransfer(image[:,:,::-1],"Models/mosaic.pth")[:,:,::-1]
	elif num == 14:
		image = styleTransfer(image[:,:,::-1],"Models/udnie.pth")[:,:,::-1]
	elif num == 15:
		fn = input("Filename?:")
		cv2.imwrite(fn, image)
	
	cv2.imshow('Image', image)
	cv2.waitKey(1)	