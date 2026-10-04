import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 4: 3D Projection Engine")
clock = pygame.time.Clock()
FPS = 60

cube_vertices = [
    [-100, -100, -100], [100, -100, -100],
    [100, 100, -100], [-100, 100, -100],
    [-100, -100, 100], [100, -100, 100],
    [100, 100, 100], [-100, 100, 100]
]

cube_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

angle_x = 0.0
angle_y = 0.0
angle_z = 0.0
mode = 1
font = pygame.font.Font(None, 30)

def rotate_x(p, angle):
    x, y, z = p
    c, s = math.cos(angle), math.sin(angle)
    return [x, y*c - z*s, y*s + z*c]

def rotate_y(p, angle):
    x, y, z = p
    c, s = math.cos(angle), math.sin(angle)
    return [x*c + z*s, y, -x*s + z*c]

def rotate_z(p, angle):
    x, y, z = p
    c, s = math.cos(angle), math.sin(angle)
    return [x*c - y*s, x*s + y*c, z]

def rotate_point(p):
    p = rotate_x(p, angle_x)
    p = rotate_y(p, angle_y)
    p = rotate_z(p, angle_z)
    return p

def project_orthographic(x, y, z):
    return int(x + WIDTH/2), int(y + HEIGHT/2)

def project_oblique(x, y, z, mode="cavalier", phi_deg=30):
    phi = math.radians(phi_deg)
    L1 = 1.0 if mode == "cavalier" else 0.5
    xp = x + z * L1 * math.cos(phi)
    yp = y + z * L1 * math.sin(phi)
    return int(xp + WIDTH/2), int(yp + HEIGHT/2)

def project_perspective(x, y, z, D=500):
    distance = z + D
    if abs(distance) < 0.001:
        distance = 0.001
    xp = (x * D) / distance
    yp = (y * D) / distance
    return int(xp + WIDTH/2), int(yp + HEIGHT/2)

def project(p):
    x, y, z = p
    if mode == 1:
        return project_orthographic(x, y, z)
    if mode == 2:
        return project_oblique(x, y, z, "cavalier")
    if mode == 3:
        return project_oblique(x, y, z, "cabinet")
    return project_perspective(x, y, z)

mode_names = {
    1: "1 - Orthographic",
    2: "2 - Cavalier Oblique",
    3: "3 - Cabinet Oblique",
    4: "4 - One-Point Perspective"
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
            elif event.key == pygame.K_3:
                mode = 3
            elif event.key == pygame.K_4:
                mode = 4

    keys = pygame.key.get_pressed()
    speed = 0.025

    if keys[pygame.K_a]:
        angle_y -= speed
    if keys[pygame.K_d]:
        angle_y += speed
    if keys[pygame.K_w]:
        angle_x -= speed
    if keys[pygame.K_s]:
        angle_x += speed
    if keys[pygame.K_q]:
        angle_z -= speed
    if keys[pygame.K_e]:
        angle_z += speed

    rotated = [rotate_point(v) for v in cube_vertices]
    projected = [project(v) for v in rotated]

    screen.fill((18, 18, 25))

    for a, b in cube_edges:
        pygame.draw.line(screen, (100, 210, 255), projected[a], projected[b], 3)

    for p in projected:
        pygame.draw.circle(screen, (255, 180, 80), p, 5)

    title = font.render(
        f"{mode_names[mode]} | 1-4 switch | W/S X | A/D Y | Q/E Z | ESC quit",
        True, (240, 240, 240)
    )
    screen.blit(title, (15, 15))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
