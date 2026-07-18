import pygame
from inter.tools import *
from inter.classes import Object3D
from math import degrees

config = get_config()

pygame.init()
WIDTH, HEIGHT = config["general"]["window_width"], config["general"]["window_height"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

focal_length = config["general"]["focal_length"]

camera_pos = [0.0, 0.0, -5.0]
camera_rot = [0.0, 0.0, 1.0, 0.0]
objects: list[Object3D] = []

objects.append(Object3D((0, 0, 0), (0, 0, 0), 90))
objects[0].load_asset("monkey")

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_pos[2] += 0.05
        if keys[pygame.K_s]:
            camera_pos[2] -= 0.05
        if keys[pygame.K_a]:
            camera_pos[0] -= 0.05
        if keys[pygame.K_d]:
            camera_pos[0] += 0.05
        if keys[pygame.K_RIGHT]:
            camera_rot[0] -= 0.05
        if keys[pygame.K_LEFT]:
            camera_rot[0] += 0.05

        for obj in objects:
            for vertex in obj.vertices:
                x, y, z = vertex
                xt, yt, zt = camera_pos
                x -= xt
                y -= yt
                z -= zt
                x += obj.pos[0]
                y += obj.pos[1]
                z += obj.pos[2]

                x, y, z = qver((camera_rot[1], camera_rot[2], camera_rot[3]), (x, y, z), degrees(camera_rot[0]))[1:]

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