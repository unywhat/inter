import pygame
from inter.tools import *
from inter.classes import Object3D

config = get_config()

pygame.init()
WIDTH, HEIGHT = config["general"]["window_width"], config["general"]["window_height"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

focal_length = config["general"]["focal_length"]
sensitivity = config["general"]["sensitivity"]

camera_pos = [0.0, 0.0, -5.0]
camera_rot = (1.0, 0.0, 0.0, 0.0)
objects: list[Object3D] = []

objects.append(Object3D((0, 0, 0), (0, 0, 0), 90))
objects[0].load_asset("sphere")

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
pygame.mouse.get_rel()

def main():
    global camera_rot
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        mouse_movement = pygame.mouse.get_rel()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            forward = qrotate(camera_rot, (0.0, 0.0, 1.0))
            camera_pos[0] += forward[0] * 0.05
            camera_pos[1] += forward[1] * 0.05
            camera_pos[2] += forward[2] * 0.05
        if keys[pygame.K_s]:
            forward = qrotate(camera_rot, (0.0, 0.0, 1.0))
            camera_pos[0] -= forward[0] * 0.05
            camera_pos[1] -= forward[1] * 0.05
            camera_pos[2] -= forward[2] * 0.05
        if keys[pygame.K_d]:
            forward = qrotate(camera_rot, (1.0, 0.0, 0.0))
            camera_pos[0] += forward[0] * 0.05
            camera_pos[1] += forward[1] * 0.05
            camera_pos[2] += forward[2] * 0.05
        if keys[pygame.K_a]:
            forward = qrotate(camera_rot, (1.0, 0.0, 0.0))
            camera_pos[0] -= forward[0] * 0.05
            camera_pos[1] -= forward[1] * 0.05
            camera_pos[2] -= forward[2] * 0.05
        if keys[pygame.K_SPACE]:
            forward = qrotate(camera_rot, (0.0, 1.0, 0.0))
            camera_pos[0] += forward[0] * 0.05
            camera_pos[1] += forward[1] * 0.05
            camera_pos[2] += forward[2] * 0.05
        if keys[pygame.K_LSHIFT]:
            forward = qrotate(camera_rot, (0.0, 1.0, 0.0))
            camera_pos[0] -= forward[0] * 0.05
            camera_pos[1] -= forward[1] * 0.05
            camera_pos[2] -= forward[2] * 0.05

        delta = atoquat((0, 1, 0), mouse_movement[0]*sensitivity)
        camera_rot = qnorm(qmul(camera_rot, delta))
        delta = atoquat((1, 0, 0), mouse_movement[1]*sensitivity)
        camera_rot = qnorm(qmul(camera_rot, delta))
                    

        for obj in objects:
            for edge in obj.edges:
                p1, p2 = [], []
                skip_edge = False

                for point in edge:
                    x, y, z = point
                    xt, yt, zt = camera_pos
                    x -= xt
                    y -= yt
                    z -= zt
                    x += obj.pos[0]
                    y += obj.pos[1]
                    z += obj.pos[2]

                    x, y, z = qrotate(qconj(camera_rot), (x, y, z))

                    if z <= 0:
                        skip_edge = True
                        break

                    (p1 if not p1 else p2).append((x, y, z))

                if skip_edge:
                    continue

                pygame.draw.aaline(
                    screen,
                    (240, 240, 240),
                    project(p1[0], focal_length, WIDTH, HEIGHT),
                    project(p2[0], focal_length, WIDTH, HEIGHT),
                    2
                )

            for vertex in obj.vertices:
                x, y, z = vertex
                xt, yt, zt = camera_pos
                x -= xt
                y -= yt
                z -= zt
                x += obj.pos[0]
                y += obj.pos[1]
                z += obj.pos[2]

                x, y, z = qrotate(qconj(camera_rot), (x, y, z))

                if z <= 0:
                    continue

                pygame.draw.aacircle(
                    screen,
                    (255, 255, 255),
                    project((x, y, z), focal_length, WIDTH, HEIGHT),
                    3
                )

        pygame.display.flip()
        clock.tick(60)