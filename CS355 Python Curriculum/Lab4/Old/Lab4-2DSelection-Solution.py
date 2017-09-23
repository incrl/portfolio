# Import a library of functions called 'pygame'
import pygame
from math import pi
from math import sin
from math import cos
from ShapesSolution import *

def drawSelection(selection):
	if selection == None:
		return
		
	s = selection
	#Making transparent drawing object
	surface = pygame.Surface([s.getWidth(),s.getHeight()], pygame.SRCALPHA, 32)
	surface = surface.convert_alpha()
	
	if isinstance(s, Rect):
		pygame.draw.rect(surface, GREEN, [0, 0, s.getWidth(), s.getHeight()], 5)		
	if isinstance(s, Square):
		pygame.draw.rect(surface, GREEN, [0, 0, s.getWidth(), s.getHeight()], 5)
	if isinstance(s, Ellipse):
		pygame.draw.ellipse(surface, GREEN, [0, 0, s.getWidth(), s.getHeight()], 5)	
	if isinstance(s, Circle):
		pygame.draw.ellipse(surface, GREEN, [0, 0, s.getWidth(), s.getHeight()], 5)
	
	#Rotate and draw on screen
	surface = pygame.transform.rotate(surface,-s.rotation)
	w,h = surface.get_size()
	topleftx = (s.center.x + (s.getWidth() - w)/2.0) - s.getWidth()/2.0
	toplefty = (s.center.y + (s.getHeight() - h)/2.0) - s.getHeight()/2.0
	screen.blit(surface, (topleftx, toplefty))	
 
 
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
ORANGE = (255, 165, 0)
PURPLE = (255, 0, 255)
 
# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
mouseDown = False
start = Point(0.0,0.0)
end = Point(0.0,0.0)
tolerance = 4
index = -1
selection = None
shapelist = []
tool = ""

#Loop until the user clicks the close button.
while not done:

	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(100)

	# Clear the screen and set the screen background
	screen.fill(BLACK)

	#Controller Code#
	#####################################################################
	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_r]:
		tool = "Rectangle"
		selection = None
	if pressed[pygame.K_s]:
		tool = "Square"
		selection = None
	if pressed[pygame.K_e]:
		tool = "Ellipse"
		selection = None
	if pressed[pygame.K_c]:
		tool = "Circle"
		selection = None
	if pressed[pygame.K_q]:
		tool = "Selection"
	if pressed[pygame.K_LEFT]:
		if selection != None:
			selection.rotation -= 3
	if pressed[pygame.K_RIGHT]:
		if selection != None:
			selection.rotation += 3
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
			mpos = pygame.mouse.get_pos()
			start.x = mpos[0]
			start.y = mpos[1]
			#Add starting shape
			if tool == "Rectangle":
				shapelist.append(Rect(ORANGE,Point(0.0,0.0),0.0,0.0))
				index = len(shapelist) - 1
			if tool == "Square":
				shapelist.append(Square(RED,Point(0.0,0.0),0.0))
				index = len(shapelist) - 1
			if tool == "Ellipse":
				shapelist.append(Ellipse(PURPLE,Point(0.0,0.0),0.0,0.0))
				index = len(shapelist) - 1
			if tool == "Circle":
				shapelist.append(Circle(BLUE,Point(0.0,0.0),0.0))
				index = len(shapelist) - 1
			#Do selection test
			if tool == "Selection":
				selection = None
				#Go through list in back to front order
				for s in shapelist[::-1]:
					if s.pointInShape(start,tolerance):
						selection = s
						break
					
			
		elif event.type == pygame.MOUSEMOTION:
			if mouseDown:
				mpos = pygame.mouse.get_pos()
				end.x = mpos[0]
				end.y = mpos[1]
				#Modify exsisting shape
				if index >= 0:
					s = shapelist[index]
					if isinstance(s, Rect):
						s.width = abs(end.x - start.x)
						s.height = abs(end.y - start.y)
						tx = min(start.x, end.x)
						ty = min(start.y, end.y)
						s.center = Point(tx + s.width/2.0, ty + s.height/2.0)
					if isinstance(s, Square):
						length_x = abs(end.x - start.x)
						length_y = abs(end.y - start.y)
						s.size = min(length_x, length_y)
						tx = min(start.x, max(end.x, start.x - s.size))
						ty = min(start.y, max(end.y, start.y - s.size))
						s.center = Point(tx + s.size/2.0, ty + s.size/2.0)
					if isinstance(s, Ellipse):
						s.width = abs(end.x - start.x)
						s.height = abs(end.y - start.y)
						tx = min(start.x, end.x)
						ty = min(start.y, end.y)
						s.center = Point(tx + s.width/2.0, ty + s.height/2.0)
					if isinstance(s, Circle):
						length_x = abs(end.x - start.x)
						length_y = abs(end.y - start.y)
						diameter = min(length_x, length_y)
						tx = min(start.x, max(end.x, start.x - diameter))
						ty = min(start.y, max(end.y, start.y - diameter))
						s.radius = diameter/2.0
						s.center = Point(tx + s.radius, ty + s.radius)
				if selection != None:
				
					selection.center.x += end.x - start.x
					selection.center.y += end.y - start.y
					start.x = end.x
					start.y = end.y
					
		elif event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False
			index = -1
	

	#Viewer Code#
	#####################################################################

	for s in shapelist:
		#Making transparent drawing object
		surface = pygame.Surface([s.getWidth(),s.getHeight()], pygame.SRCALPHA, 32)
		surface = surface.convert_alpha()
		
		if isinstance(s, Rect):
			pygame.draw.rect(surface, s.color, [0, 0, s.getWidth(), s.getHeight()])		
		if isinstance(s, Square):
			pygame.draw.rect(surface, s.color, [0, 0, s.getWidth(), s.getHeight()])
		if isinstance(s, Ellipse):
			pygame.draw.ellipse(surface, s.color, [0, 0, s.getWidth(), s.getHeight()])	
		if isinstance(s, Circle):
			pygame.draw.ellipse(surface, s.color, [0, 0, s.getWidth(), s.getHeight()])
		
		#Rotate and draw on screen
		surface = pygame.transform.rotate(surface,-s.rotation)
		w,h = surface.get_size()
		topleftx = (s.center.x + (s.getWidth() - w)/2.0) - s.getWidth()/2.0
		toplefty = (s.center.y + (s.getHeight() - h)/2.0) - s.getHeight()/2.0
		screen.blit(surface, (topleftx, toplefty))	

	drawSelection(selection)

	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()

# Be IDLE friendly
pygame.quit()

