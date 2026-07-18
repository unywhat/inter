import pygame
from inter.tools import *

config = get_config()

pygame.init()
WIDTH, HEIGHT = config["general"]["window_width"], config["general"]["window_height"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

focal_length = config["general"]["focal_length"]

def project(pos: tuple[float, float, float]):
    x, y, z = pos
    screen_x = WIDTH / 2 + focal_length * (x / z)
    screen_y = HEIGHT / 2 - focal_length * (y / z)
    return (screen_x, screen_y)


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
                project((x, y, z)),
                3
            )

        pygame.display.flip()
        clock.tick(60)