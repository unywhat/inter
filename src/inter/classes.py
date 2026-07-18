from math import radians
from inter.tools import load_asset

class Object3D:
    def __init__(self, pos: tuple[float, float, float], rotation_axis: tuple[float, float, float], rotation_degrees: float):
        self.pos = list(pos)
        self.axis = rotation_axis
        self.deg = radians(rotation_degrees)
        self.edges: list[tuple[tuple[float, float, float], tuple[float, float, float]]] = []

        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0

        self.mass = 1.0

    def load_asset(self, name: str):
        self.vertices, self.edges = load_asset(name)

    def update(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az

        self.pos[0] += self.vx
        self.pos[1] += self.vy
        self.pos[2] += self.vz