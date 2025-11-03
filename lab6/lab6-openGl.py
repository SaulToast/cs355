import sys
import numpy as np

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import glPushMatrix
    from OpenGL.GL import glPopMatrix
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

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


DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
M_SECONDS = 32

cam = Camera(position=[-50, -5, -24], rotY=-70)
isOrtho = False
time = 0

def incrementTime(value):
    global time
    time += value
    glutTimerFunc(M_SECONDS, incrementTime, 1)
    glutPostRedisplay()

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawCar():
	glLineWidth(2.5)
	glColor3f(0.0, 1.0, 0.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-3, 2, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 2, 2)
	#Back Side
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 2, -2)
	#Connectors
	glVertex3f(-3, 2, 2)
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, -2)
	glEnd()
	
def drawTire():
	glLineWidth(2.5)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-1, .5, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, .5, .5)
	#Back Side
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, .5, -.5)
	#Connectors
	glVertex3f(-1, .5, .5)
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, -.5)
	glEnd()
		
def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

def drawWithPush(drawFunc, *transforms):
    """
    Takes in a draw function and any amount of transformations as lambda functions.
    Pushes the current matrix, Applies Transformations, Calls the draw function, Pops the Matrix.
    """

    glPushMatrix()
    for t in transforms:
        t()
    drawFunc()
    glPopMatrix()

def displayStreet():
    drawWithPush(drawHouse)
    drawWithPush(drawHouse,
                 lambda: glTranslated(12, 0, 0))
    drawWithPush(drawHouse,
                 lambda: glTranslated(-12, 0, 0))
    drawWithPush(drawHouse,
                 lambda: glTranslated(-24, 0, 12),
                 lambda: glRotated(90, 0, 1, 0))
    drawWithPush(drawHouse, 
                 lambda: glTranslated(0, 0, 24),
                 lambda: glRotated(180, 0, 1, 0))
    drawWithPush(drawHouse, 
                 lambda: glTranslated(12, 0, 24),
                 lambda: glRotated(180, 0, 1, 0))
    drawWithPush(drawHouse, 
                 lambda: glTranslated(-12, 0, 24),
                 lambda: glRotated(180, 0, 1, 0))

def displayCar():
    drawWithPush(displayCarHelper,
                 lambda: glTranslated(time/4, 0, 12))

def displayCarHelper():
    """
    Passed into the drawWithPush function from displayCar 
    allowing it to draw the car and the tires with correct matrix stack order
    """
    drawCar()
    drawWithPush(drawTire,
                 lambda: glTranslated(2, 0, 2),
                 lambda: glRotated(-time * 1.3, 0, 0, 1))
    drawWithPush(drawTire,
                 lambda: glTranslated(2, 0, -2),
                 lambda: glRotated(-time * 1.3, 0, 0, 1))
    drawWithPush(drawTire,
                 lambda: glTranslated(-2, 0, 2),
                 lambda: glRotated(-time * 1.3, 0, 0, 1))
    drawWithPush(drawTire,
                 lambda: glTranslated(-2, 0, -2),
                 lambda: glRotated(-time * 1.3, 0, 0, 1))

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 
    #Your Code Here

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if not isOrtho:
        gluPerspective(45, DISPLAY_HEIGHT/DISPLAY_WIDTH, 0.1, 100)
    else:
        glOrtho(-10, 10, -10, 10, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotated(cam.rotX, 1, 0, 0)
    glRotated(cam.rotY, 0, 1, 0)
    glTranslated(cam.position[0], cam.position[1], cam.position[2])
    
    displayStreet()
    displayCar()

    glFlush()
    
def keyboard(key, x, y):
    global cam, isOrtho, time

    if key == chr(27):
        import sys
        sys.exit(0)
    
    speed = 1
    if key == b'w':
        cam.position[0] -= cam.forward[0] * speed
        cam.position[1] -= cam.forward[1] * speed
        cam.position[2] -= cam.forward[2] * speed
    if key == b's':
        cam.position[0] += cam.forward[0] * speed
        cam.position[1] += cam.forward[1] * speed
        cam.position[2] += cam.forward[2] * speed
    if key == b'a':
        cam.position[0] += cam.right[0] * speed
        cam.position[1] += cam.right[1] * speed
        cam.position[2] += cam.right[2] * speed
    if key == b'd':
        cam.position[0] -= cam.right[0] * speed
        cam.position[1] -= cam.right[1] * speed
        cam.position[2] -= cam.right[2] * speed
    if key == b'e':
        cam.rotY += 5
    if key == b'q':
        cam.rotY -= 5
    # added forward and backward tilt to move around scene better
    if key == b't':
        cam.rotX -= 5
    if key == b'g':
        cam.rotX += 5
    if key == b'f':
        cam.position[0] += cam.up[0] * speed
        cam.position[1] += cam.up[1] * speed
        cam.position[2] += cam.up[2] * speed
    if key == b'r':
        cam.position[0] -= cam.up[0] * speed
        cam.position[1] -= cam.up[1] * speed
        cam.position[2] -= cam.up[2] * speed
    if key == b'h':
        cam.reset()
        time = 0
    if key == b'o':
        isOrtho = True
    if key == b'p':
        isOrtho = False
  
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition(100, 100)
glutCreateWindow(b'OpenGL Lab')
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(M_SECONDS, incrementTime, 1)
glutMainLoop()
