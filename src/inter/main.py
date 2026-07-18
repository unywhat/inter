import pygame
from inter.tools import *

config = get_config()

pygame.init()
WIDTH, HEIGHT = config["general"]["window_width"], config["general"]["window_height"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

focal_length = config["general"]["focal_length"]

camera_pos = (0, 0, -2)

cube_points = [
    (-1, -1, 3),
    ( 1, -1, 3),
    ( 1,  1, 3),
    (-1,  1, 3),
    (-1, -1, 5),
    ( 1, -1, 5),
    ( 1,  1, 5),
    (-1,  1, 5),
]

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        for point in cube_points:
            x, y, z = point
            xt, yt, zt = camera_pos
            x -= xt
            y -= yt
            z -= zt
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