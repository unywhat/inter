from math import sin, cos, radians

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
    """Project a 3D point into a 2D coordinate.
    
    Parameters:
        3-tuple: orginal position.
        float: focal length.
        int: width of screen.
        int: height of screen.

    Returns:
        2-tuple: projected coordinates.
    """

    x, y, z = pos

    screen_x = w / 2 + f * (x / z)
    screen_y = h / 2 - f * (y / z)

    return (screen_x, screen_y)

def load_asset(name: str) -> list[tuple[float, float, float]]:
    """Loads and returns one of the saved assets.
    Asset folder: models/ (project root)
    
    Parameters:
        str: the name of the asset to return.
    
    Returns:
        list: list of 3-tuples containing vertex data.
    """

    extracted_points: list[tuple[float, float, float]] = []

    with open(f'models/{name}.inter', 'r') as obj:
        for line in obj:
            x, y, z = line.split()
            extracted_points.append((float(x), float(y), float(z)))

    return extracted_points

def convert_obj_to_inter(name: str):
    """Converts OBJ files to .inter.
    Saves converted OBJ files to models/
    Limited to just vertices currently.

    Parameters:
        str: name of the file in the project root directory.

    Returns:
        list: list of 3-tuples with coordinates.
    """

    inter_coords: list[tuple[float, float, float]] = []

    with open(f'{name}.obj', 'r') as obj:
        for line in obj:
            if line[0] == "v":
                split_line = line.split()
                coordinates = split_line[1:]
                x, y, z = coordinates

                inter_coords.append((float(x), float(y), float(z)))

    with open(f'models/{name}.inter', 'a') as inter_file:
        for coordinate in inter_coords:
            x, y, z = coordinate
            inter_file.write(f'{x} {y} {z}\n')

    return inter_coords