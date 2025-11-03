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
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

class Camera:

    def __init__(self, position = [0.0, 0.0, 0.0], rotY = 0, rotX = 0):
        self.position = position
        self.rotY = rotY
        self.rotX = rotX
    
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

cam = Camera()
isOrtho = False

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

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
    glRotated(cam.rotY, 0, 1, 0)
    glTranslated(0, -5, -20)
    glTranslated(cam.position[0], cam.position[1], cam.position[2])
    
    
    drawHouse()

    
    glFlush()
    

def keyboard(key, x, y):
    global cam, isOrtho

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
    if key == b'f':
        cam.position[0] += cam.up[0] * speed
        cam.position[1] += cam.up[1] * speed
        cam.position[2] += cam.up[2] * speed
    if key == b'r':
        cam.position[0] -= cam.up[0] * speed
        cam.position[1] -= cam.up[1] * speed
        cam.position[2] -= cam.up[2] * speed
    if key == b'h':
        cam.position = [0, 0, 0]
        cam.rotY = 0
    if key == b'o':
        isOrtho = True
    if key == b'p':
        isOrtho = False
  
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
