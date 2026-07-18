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

def qmul(q1: tuple[float, float, float, float], q2: tuple[float, float, float, float]):
    """Multiply two quaternions together and return the result.

    Parameters:
        4-tuple: quaternion 1.
        4-tuple: quaternion 2.

    Returns:
        4-tuple: multiplied quaternion.
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return (
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    )

def atoquat(axis: tuple[float, float, float], angle_deg: float) -> tuple[float, float, float, float]:
    angle = radians(angle_deg)
    s = sin(angle / 2)
    return (cos(angle / 2), axis[0]*s, axis[1]*s, axis[2]*s)

def qrotate(q: tuple[float, float, float, float], vertex: tuple[float, float, float]) -> tuple[float, float, float]:
    """Rotate a 3D vector by an already made quaternion.

    Parameters:
        4-tuple: the rotation quaternion (w, x, y, z).
        3-tuple: the vertex to rotate.

    Returns:
        3-tuple: the rotated vertex (x, y, z).
    """

    w, x, y, z = q
    q_conj = (w, -x, -y, -z)
    v = (0.0, *vertex)

    qv = (
        q[0]*v[0] - q[1]*v[1] - q[2]*v[2] - q[3]*v[3],
        q[0]*v[1] + q[1]*v[0] + q[2]*v[3] - q[3]*v[2],
        q[0]*v[2] - q[1]*v[3] + q[2]*v[0] + q[3]*v[1],
        q[0]*v[3] + q[1]*v[2] - q[2]*v[1] + q[3]*v[0],
    )

    result = (
        qv[0]*q_conj[0] - qv[1]*q_conj[1] - qv[2]*q_conj[2] - qv[3]*q_conj[3],
        qv[0]*q_conj[1] + qv[1]*q_conj[0] + qv[2]*q_conj[3] - qv[3]*q_conj[2],
        qv[0]*q_conj[2] - qv[1]*q_conj[3] + qv[2]*q_conj[0] + qv[3]*q_conj[1],
        qv[0]*q_conj[3] + qv[1]*q_conj[2] - qv[2]*q_conj[1] + qv[3]*q_conj[0],
    )

    return result[1:]

def qconj(q: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    w, x, y, z = q
    return (w, -x, -y, -z)

def qnorm(q: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Normalize a quaternion to unit length, preventing drift from accumulated rotations.

    Parameters:
        4-tuple: the quaternion (w, x, y, z).

    Returns:
        4-tuple: the normalized quaternion (w, x, y, z).
    """
    w, x, y, z = q
    mag = (w*w + x*x + y*y + z*z) ** 0.5
    return (w/mag, x/mag, y/mag, z/mag)

def qver(axis: tuple[float, float, float], vertex: tuple[float, float, float], angle: float) -> tuple[float, float, float, float]:
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

def load_asset(name: str) -> tuple[list[tuple[float, float, float]], list[tuple[tuple[float, float, float], tuple[float, float, float]]]]:
    """Loads and returns one of the saved assets.
    Asset folder: models/ (project root)
    
    Parameters:
        str: the name of the asset to return.
    
    Returns:
        list: list of 3-tuples containing vertex data.
    """

    extracted_points: list[tuple[float, float, float]] = []
    extracted_edges: list[tuple[int, int]] = []

    with open(f'models/{name}.inter', 'r') as obj:
        section = "vertices"

        for line in obj:
            sp_line = line.split()
            if not sp_line:
                section = "edges"
                continue

            if section == "vertices":
                x, y, z = sp_line
                extracted_points.append((float(x), float(y), float(z)))

            elif section == "edges":
                edge = line.strip().split("-")
                extracted_edges.append((int(edge[0]), int(edge[1])))

    resolved_edges = [
        (extracted_points[a], extracted_points[b])
        for a, b in extracted_edges
    ]

    return extracted_points, resolved_edges

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