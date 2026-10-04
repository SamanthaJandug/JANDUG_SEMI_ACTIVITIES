import pygame
import math
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Activity 1: 2D Animation, Tweening & Morphing Engine")
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
FPS = 60

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_point(p1, p2, t):
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def ease_in_out(t):
    return t * t * (3 - 2 * t)

def path_position(points, progress):
    """Linear interpolation along a multi-point path."""
    if progress <= 0:
        return points[0]
    if progress >= 1:
        return points[-1]

    scaled = progress * (len(points) - 1)
    i = min(int(scaled), len(points) - 2)
    local_t = scaled - i
    return lerp_point(points[i], points[i + 1], local_t)

# Equalized 4-vertex keyframes.
# The triangle is represented with a subdivided edge, as required by
# the vertex correspondence rule.
triangle = [(200, 100), (250, 200), (300, 300), (100, 300)]
rectangle = [(150, 100), (350, 120), (320, 320), (120, 300)]

path = [(100, 150), (250, 100), (400, 250), (550, 150), (700, 350)]

ball_x, ball_y = 600.0, 100.0
ball_vel_x, ball_vel_y = 2.5, 0.0
gravity = 0.5
restitution = 0.78
floor_y = 500
ball_radius = 20

mode = 1
morph_t = 0.0
morph_direction = 1
path_t = 0.0
font = pygame.font.Font(None, 28)

def draw_tweening():
    global path_t
    path_t = (path_t + 0.004) % 1.0

    x, y = path_position(path, ease_in_out(path_t))

    pygame.draw.lines(screen, (100, 100, 100), False, path, 3)
    for p in path:
        pygame.draw.circle(screen, (150, 150, 150), p, 5)

    pygame.draw.circle(screen, (50, 150, 255), (int(x), int(y)), 22)

def draw_morphing():
    global morph_t, morph_direction
    morph_t += 0.01 * morph_direction
    if morph_t >= 1:
        morph_t = 1
        morph_direction = -1
    elif morph_t <= 0:
        morph_t = 0
        morph_direction = 1

    t = ease_in_out(morph_t)
    poly = [lerp_point(a, b, t) for a, b in zip(triangle, rectangle)]

    pygame.draw.polygon(screen, (80, 180, 255), poly)
    pygame.draw.polygon(screen, (255, 255, 255), poly, 3)
    for p in poly:
        pygame.draw.circle(screen, (255, 100, 100), (int(p[0]), int(p[1])), 6)

def draw_dynamics():
    global ball_x, ball_y, ball_vel_x, ball_vel_y

    ball_vel_y += gravity
    ball_x += ball_vel_x
    ball_y += ball_vel_y

    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_vel_x *= -1

    if ball_y + ball_radius >= floor_y:
        ball_y = floor_y - ball_radius
        ball_vel_y = -restitution * ball_vel_y

    pygame.draw.line(screen, (100, 100, 100), (0, floor_y), (WIDTH, floor_y), 3)
    pygame.draw.circle(screen, (255, 100, 80), (int(ball_x), int(ball_y)), ball_radius)

def draw_ui():
    names = {1: "Tweening", 2: "Morphing", 3: "Dynamics"}
    text = font.render(
        f"Mode: {names[mode]}   |   Press 1, 2, 3 to switch   |   ESC to quit",
        True, (240, 240, 240)
    )
    screen.blit(text, (15, 15))

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

    screen.fill((25, 25, 35))

    if mode == 1:
        draw_tweening()
    elif mode == 2:
        draw_morphing()
    else:
        draw_dynamics()

    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
