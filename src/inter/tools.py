def get_config():
    """Load and return config data from inter.toml.

    Returns:
        dict: config data from inter.toml
    """

    import tomllib

    with open('inter.toml', 'rb') as cfg:
        data = tomllib.load(cfg)

    return data

def qmul(axis: tuple[float, float, float], vertex: tuple[float, float, float], angle: float) -> tuple[float, float, float, float]:
    """Rotate a 3D vector by an axis-angle quaternion.

    Parameters:
        3-tuple: the rotation axis (x, y, z).
        3-tuple: the vertex to rotate.
        float: rotation angle in degrees.

    Returns:
        4-tuple: the rotated quaternion (w, x, y, z).
    """
    from math import sin, cos, radians
    angle = radians(angle)
    q = (cos(angle/2), axis[0]*sin(angle/2), axis[1]*sin(angle/2), axis[2]*sin(angle/2))
    v = (0, *vertex)

    rotated_v = (
        q[0]*v[0] - q[1]*v[1] - q[2]*v[2] - q[3]*v[3],
        q[0]*v[1] + q[1]*v[0] + q[2]*v[3] - q[3]*v[2],
        q[0]*v[2] - q[1]*v[3] + q[2]*v[0] + q[3]*v[1],
        q[0]*v[3] + q[1]*v[2] - q[2]*v[1] + q[3]*v[0],
    )

    q = (cos(angle/2), -axis[0]*sin(angle/2), -axis[1]*sin(angle/2), -axis[2]*sin(angle/2))

    rotated_v = (
        rotated_v[0]*q[0] - rotated_v[1]*q[1] - rotated_v[2]*q[2] - rotated_v[3]*q[3],
        rotated_v[0]*q[1] + rotated_v[1]*q[0] + rotated_v[2]*q[3] - rotated_v[3]*q[2],
        rotated_v[0]*q[2] - rotated_v[1]*q[3] + rotated_v[2]*q[0] + rotated_v[3]*q[1],
        rotated_v[0]*q[3] + rotated_v[1]*q[2] - rotated_v[2]*q[1] + rotated_v[3]*q[0],
    )

    return rotated_v

def project(pos: tuple[float, float, float], f: float, w: int, h: int):
    x, y, z = pos
    screen_x = w / 2 + f * (x / z)
    screen_y = h / 2 - f * (y / z)
    return (screen_x, screen_y)