import pygame
import math
import sys

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Activity 1: 2D Animation, Tweening & Morphing Engine')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# --- 1.1 Helper Functions ---
def lerp(a, b, t):
    return a + (b - a) * t

def lerp_point(p1, p2, t):
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def ease_in_out(t):
    # Smoothstep interpolation
    return t * t * (3 - 2 * t)

# --- Task 1.1: Multi-point Spline/Path Tweening ---
path_points = [(100, 100), (300, 150), (500, 100), (700, 300), (500, 500), (200, 450)]
path_t = 0.0
path_speed = 0.005  # Speed of parameter progression

def get_point_on_path(points, t_global):
    # Parameter t ranges from 0.0 to 1.0 across the entire path
    num_segments = len(points) - 1
    scaled_t = t_global * num_segments
    segment_idx = min(int(scaled_t), num_segments - 1)
    segment_t = scaled_t - segment_idx
    # Apply Ease-In-Out for smoother movement
    smooth_t = ease_in_out(segment_t)
    return lerp_point(points[segment_idx], points[segment_idx + 1], smooth_t)

# --- Task 1.2: Polygon Morphing (Triangle -> Quadrilateral) ---
# Vertex Correspondence Rule: Triangle has 4 vertices with a midpoint split along top edge
poly_start = [(200, 100), (250, 100), (300, 300), (100, 300)]  # Triangle (4 control vertices)
poly_end   = [(150, 100), (350, 150), (300, 350), (100, 300)]  # Quadrilateral
morph_t = 0.0
morph_dir = 1

# --- Task 1.3: Dynamics Bouncing Ball ---
ball_x, ball_y = 600.0, 100.0
ball_vel_x = 2.0
ball_vel_y = 0.0
gravity = 0.5
restitution = 0.78  # Coefficient of restitution (e)
floor_y = 500
ball_radius = 15

# Global State Toggle (Keys 1, 2, 3)
mode = 1  # 1: Tweening, 2: Morphing, 3: Dynamics

# Main Loop
running = True
while running:
    clock.tick(60)  # 60 FPS capping
    screen.fill((30, 30, 35))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
            elif event.key == pygame.K_3:
                mode = 3
                # Reset ball position
                ball_x, ball_y = 600.0, 100.0
                ball_vel_x, ball_vel_y = 2.0, 0.0

    # --- Mode 1: Tweening Engine ---
    if mode == 1:
        path_t += path_speed
        if path_t > 1.0:
            path_t = 0.0
        
        current_pos = get_point_on_path(path_points, path_t)

        # Draw Path
        for i in range(len(path_points) - 1):
            pygame.draw.line(screen, (100, 100, 100), path_points[i], path_points[i+1], 2)
        for pt in path_points:
            pygame.draw.circle(screen, (200, 80, 80), pt, 5)

        # Draw Moving Sprite
        pygame.draw.circle(screen, (0, 220, 180), (int(current_pos[0]), int(current_pos[1])), 16)

    # --- Mode 2: Polygon Morphing ---
    elif mode == 2:
        morph_t += 0.01 * morph_dir
        if morph_t >= 1.0 or morph_t <= 0.0:
            morph_dir *= -1
            morph_t = max(0.0, min(1.0, morph_t))

        # Interpolate Vertices
        current_poly = [lerp_point(poly_start[i], poly_end[i], morph_t) for i in range(4)]

        # Draw Morphed Polygon
        pygame.draw.polygon(screen, (100, 180, 240), current_poly)
        pygame.draw.polygon(screen, (255, 255, 255), current_poly, 2)
        for pt in current_poly:
            pygame.draw.circle(screen, (255, 100, 100), (int(pt[0]), int(pt[1])), 4)

    # --- Mode 3: Dynamics Simulation ---
    elif mode == 3:
        # Newtonian Physics Euler Integration
        ball_vel_y += gravity
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        # Floor Collision Detection & Elastic Restitution Decay
        if ball_y + ball_radius >= floor_y:
            ball_y = floor_y - ball_radius
            ball_vel_y = -ball_vel_y * restitution

        # Boundary bounce horizontal
        if ball_x + ball_radius >= SCREEN_WIDTH or ball_x - ball_radius <= 0:
            ball_vel_x *= -1

        # Draw Floor & Ball
        pygame.draw.line(screen, (200, 200, 200), (0, floor_y), (SCREEN_WIDTH, floor_y), 4)
        pygame.draw.circle(screen, (240, 200, 80), (int(ball_x), int(ball_y)), ball_radius)

    # Render HUD Information
    info_txt = font.render(f"Mode: {mode} (Press 1: Tweening | 2: Morphing | 3: Dynamics) | FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(info_txt, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()