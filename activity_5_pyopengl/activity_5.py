import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Activity 5: Hardware Pipeline with PyOpenGL")

gluPerspective(45, display[0] / display[1], 0.1, 50.0)
glTranslatef(0.0, 0.0, -7)

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

vertices = [
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
]

colors = [
    (1,0,0), (0,1,0), (0,0,1), (1,1,0),
    (1,0,1), (0,1,1), (1,1,1), (0.5,0.5,0.5)
]

surfaces = [
    (0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6)
]

rotation = 0.0
clock = pygame.time.Clock()

def draw_colored_cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex_idx in surface:
            glColor4f(*colors[vertex_idx], 0.90)
            glVertex3fv(vertices[vertex_idx])
    glEnd()

def draw_articulated_arm():
    # Hierarchical modeling using push/pop matrix.
    glPushMatrix()

    # Shoulder/base
    glTranslatef(-2.2, 0.0, 0.0)
    glRotatef(rotation, 0, 1, 0)

    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)
    glColor4f(1, 0.5, 0.2, 0.9)
    draw_colored_cube()
    glPopMatrix()

    # Upper arm
    glTranslatef(0.9, 0.0, 0.0)
    glRotatef(rotation * 0.5, 0, 0, 1)

    glPushMatrix()
    glScalef(1.0, 0.25, 0.25)
    glColor4f(0.2, 0.8, 1.0, 0.75)
    draw_colored_cube()
    glPopMatrix()

    # Forearm
    glTranslatef(1.0, 0.0, 0.0)
    glRotatef(rotation * 0.7, 0, 0, 1)

    glPushMatrix()
    glScalef(0.8, 0.2, 0.2)
    glColor4f(0.8, 0.2, 1.0, 0.75)
    draw_colored_cube()
    glPopMatrix()

    glPopMatrix()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    rotation += 1.0

    # Clear BOTH color and depth buffers every frame.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(rotation, 1, 1, 0)
    draw_colored_cube()
    glPopMatrix()

    draw_articulated_arm()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
