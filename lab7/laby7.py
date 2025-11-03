# Import a library of functions called 'pygame'
import pygame
from math import pi
import numpy as np

class Camera:

    def __init__(self, position = None, rotY = 0, rotX = 0):
        if position is None:
            position = [0,0,0]

        self.position = position[:]
        self.defaultPosition = position[:]
        self.rotY = rotY
        self.defaultRotY = rotY
        self.rotX = rotX
        self.defaultRotX = rotX
    
    def reset(self):
        self.position = self.defaultPosition[:]
        self.rotY = self.defaultRotY
        self.rotX = self.defaultRotX

    @property
    def forward(self):
        rotXRads = np.radians(self.rotX)
        rotYRads = np.radians(self.rotY)
        x = np.sin(rotYRads) * np.cos(rotXRads)
        y = np.sin(rotXRads)
        z = -np.cos(rotYRads) * np.cos(rotXRads)
        return [x, y, z]
    
    @property
    def right(self):
        rotYRads = np.radians(self.rotY)
        x = np.cos(rotYRads)
        y = 0
        z = np.sin(rotYRads)
        return [x, y, z]
    
    @property
    def up(self):
        r = self.right
        f = self.forward
        return np.cross(np.array(r), np.array(f))

class MatrixStack:
	def __init__(self):
		self.stack = [np.identity(4)]
		
	def loadIdentity(self):
		self.stack[-1] = np.identity(4)
		
	def push(self):
		self.stack.append(self.stack[-1].copy())
		
	def pop(self):
		if len(self.stack) > 1:
			self.stack.pop()
			
	def multiplyMatrix(self, matrix):
		self.stack[-1] = self.stack[-1] @ matrix
	
	@property
	def top(self):
		return self.stack[-1]
	
class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		
class Line3D():
	def __init__(self, start, end):
		self.start = start
		self.end = end

def loadOBJ(filename):
	
	vertices = []
	indices = []
	lines = []
	
	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
			
		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))
			
	f.close()
	
	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
		
	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]
			
			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)
					
	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]
	
	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]
	
	return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    
    return tire

def translate(x, y, z):
	m = np.identity(4)
	m[0, 3] = x
	m[1, 3] = y
	m[2, 3] = z
	return m

def rotateY(angle):
	theta = np.radians(angle)
	c = np.cos(theta)
	s = np.sin(theta)
	return np.array([
		[c, 0, s, 0],
		[0,1,0,0],
		[-s, 0, c, 0],
		[0,0,0,1]
	])
def rotateX(angle):
	theta = np.radians(angle)
	c = np.cos(theta)
	s = np.sin(theta)
	return np.array([
		[1, 0, 0, 0],
		[0,c,-s,0],
		[0, s, c, 0],
		[0,0,0,1]
	])
def rotateZ(angle):
	theta = np.radians(angle)
	c = np.cos(theta)
	s = np.sin(theta)
	return np.array([
		[c, -s, 0, 0],
		[s,c,0,0],
		[0, 0, 1, 0],
		[0,0,0,1]
	])

def perspective(fov, aspect, near, far):
	f = 1/np.tan(np.radians(fov) / 2)
	return np.array([
		[f/aspect, 0, 0, 0], 
		[0, f, 0, 0], 
		[0, 0, (far+near)/(near-far), (2*far*near)/(near-far)], 
		[0, 0, -1, 0]])

def ndcToScreen(ndc):
    x = int((ndc[0] + 1) * 0.5 * DISPLAY_WIDTH)
    y = int((1 - (ndc[1] + 1) * 0.5) * DISPLAY_HEIGHT)  # flip Y
    return (x, y)

def clipCheck(vertex):
	w = vertex[3]
	return (-w <= vertex[0] <= w) and (-w <= vertex[1] <= w) and (-w <= vertex[2] <= w)

def drawWithPush(drawFunc, *transforms):
    modelViewStack.push()
    for t in transforms:
        modelViewStack.multiplyMatrix(t)
    drawFunc()
    modelViewStack.pop()

def drawObject(lines, color):
	for s in lines:
		start_h = np.array([s.start.x, s.start.y, s.start.z, 1.0])
		end_h = np.array([s.end.x, s.end.y, s.end.z, 1.0])

		start_cam = modelViewStack.top @ start_h
		end_cam = modelViewStack.top @ end_h

		start_clip = projectionStack.top @ start_cam
		end_clip = projectionStack.top @ end_cam

		if clipCheck(start_clip) and clipCheck(end_clip):
			start_ndc = start_clip[:3] / start_clip[3]
			end_ndc = end_clip[:3] / end_clip[3]

			start_screen = ndcToScreen(start_ndc)
			end_screen = ndcToScreen(end_ndc)

			pygame.draw.line(screen, color, start_screen, end_screen)

def displayStreet():
    drawWithPush(lambda: drawObject(loadHouse(), RED))
    drawWithPush(lambda: drawObject(loadHouse(), RED),
                 translate(12, 0, 0))
    drawWithPush(lambda: drawObject(loadHouse(), RED),
                 translate(-12, 0, 0))
    drawWithPush(lambda: drawObject(loadHouse(), RED),
                 translate(-24, 0, 12),
                 rotateY(90))
    drawWithPush(lambda: drawObject(loadHouse(), RED), 
                 translate(0, 0, 24),
                 rotateY(180))
    drawWithPush(lambda: drawObject(loadHouse(), RED), 
                 translate(12, 0, 24),
                 rotateY(180))
    drawWithPush(lambda: drawObject(loadHouse(), RED), 
                 translate(-12, 0, 24),
                 rotateY(180))

def displayCar():
    drawWithPush(displayCarHelper,
                 translate(totalTime/4, 0, 12))
	
def displayCarHelper():
    """
    Passed into the drawWithPush function from displayCar 
    allowing it to draw the car and the tires with correct matrix stack order
    """
    drawObject(loadCar(), BLUE)
    drawWithPush(lambda: drawObject(loadTire(), GREEN),
                 translate(2, 0, 2),
                 rotateZ(-totalTime * 1.3))
    drawWithPush(lambda: drawObject(loadTire(), GREEN),
                 translate(2, 0, -2),
                 rotateZ(-totalTime * 1.3))
    drawWithPush(lambda: drawObject(loadTire(), GREEN),
                 translate(-2, 0, 2),
                 rotateZ(-totalTime * 1.3))
    drawWithPush(lambda: drawObject(loadTire(), GREEN),
                 translate(-2, 0, -2),
                 rotateZ(-totalTime * 1.3))
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
DISPLAY_HEIGHT = 512
DISPLAY_WIDTH = 512

# Set the height and width of the screen
size = [DISPLAY_HEIGHT, DISPLAY_WIDTH]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)

cam = Camera(position=[-50, -5, -24], rotY=-70)
projectionStack = MatrixStack()
persMatrix  = perspective(45, DISPLAY_WIDTH/DISPLAY_HEIGHT, 0.1, 100)
projectionStack.multiplyMatrix(persMatrix)
modelViewStack = MatrixStack()
totalTime = 0

#Loop until the user clicks the close button.
while not done:
 
	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	deltaMs = clock.tick(100)
	deltaSecs = deltaMs / 10
	totalTime += deltaSecs

	# Clear the screen and set the screen background
	screen.fill(BLACK)

	#Controller Code#
	#####################################################################

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True
			
	pressed = pygame.key.get_pressed()

	speed = 0.5
	if pressed[pygame.K_w]:
		cam.position[0] -= cam.forward[0] * speed
		cam.position[1] -= cam.forward[1] * speed
		cam.position[2] -= cam.forward[2] * speed
	if pressed[pygame.K_s]:
		cam.position[0] += cam.forward[0] * speed
		cam.position[1] += cam.forward[1] * speed
		cam.position[2] += cam.forward[2] * speed
	if pressed[pygame.K_a]:
		cam.position[0] += cam.right[0] * speed
		cam.position[1] += cam.right[1] * speed
		cam.position[2] += cam.right[2] * speed
	if pressed[pygame.K_d]:
		cam.position[0] -= cam.right[0] * speed
		cam.position[1] -= cam.right[1] * speed
		cam.position[2] -= cam.right[2] * speed
	if pressed[pygame.K_e]:
		cam.rotY += 1
	if pressed[pygame.K_q]:
		cam.rotY -= 1
    # added forward and backward tilt to move around scene better
	if pressed[pygame.K_f]:
		cam.position[0] += cam.up[0] * speed
		cam.position[1] += cam.up[1] * speed
		cam.position[2] += cam.up[2] * speed
	if pressed[pygame.K_r]:
		cam.position[0] -= cam.up[0] * speed
		cam.position[1] -= cam.up[1] * speed
		cam.position[2] -= cam.up[2] * speed
	if pressed[pygame.K_h]:
		cam.reset()
		totalTime = 0
        

	#Viewer Code#
	#####################################################################

	modelViewStack.loadIdentity()
	modelViewStack.multiplyMatrix(rotateY(cam.rotY))
	modelViewStack.multiplyMatrix(translate(cam.position[0], cam.position[1], cam.position[2]))

	displayStreet()
	displayCar()

	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()
