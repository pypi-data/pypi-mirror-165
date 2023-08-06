import numpy as np
from eulerangles import matrix2euler

def rotation_matrix_from_vectors(vec1: np.array, vec2: np.array):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    if any(v):  # if not all zeros then
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    else:
        return np.eye(3)

def _main_():
    a = np.array([0, 1, 0])
    b = np.array([0, 0, 1])
    rot_mat = rotation_matrix_from_vectors(a, b)
    print("First rotation matrix:")
    print(rot_mat)

    eulers = matrix2euler(rot_mat,
                          axes='zyz',
                          intrinsic=True,
                          right_handed_rotation=True)
    print("matrix2euler output for first rotation matrix:", eulers)

    a = np.array([0.0000001, 1, 0])
    b = np.array([0, 0, 1])
    rot_mat = rotation_matrix_from_vectors(a, b)
    print("Second rotation matrix")
    print(rot_mat)

    eulers = matrix2euler(rot_mat,
                          axes='zyz',
                          intrinsic=True,
                          right_handed_rotation=True)
    print("matrix2euler output for second rotation matrix:",eulers)

if __name__ == "__main__":
    _main_()
