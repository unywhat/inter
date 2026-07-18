from math import radians
from inter.tools import load_asset

class Object3D:
    def __init__(self, pos: tuple[float, float, float], rotation_axis: tuple[float, float, float], rotation_degrees: float):
        self.pos = pos
        self.axis = rotation_axis
        self.deg = radians(rotation_degrees)
        self.vertices: list[tuple[float, float, float]] = []
        self.edges: list[tuple[int, int]] = []

    def load_asset(self, name: str):
        self.vertices, self.edges = load_asset(name)