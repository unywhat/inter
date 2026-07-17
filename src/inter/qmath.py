from math import sin, cos, radians
def qmul(axis: tuple[float, float, float], vector: tuple[float, float, float], angle: float) -> tuple[float, float, float, float]:
    angle = radians(angle)
    q = (cos(angle/2), axis[0]*sin(angle/2), axis[1]*sin(angle/2), axis[2]*sin(angle/2))
    v = (0, *vector)

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