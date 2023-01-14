import numpy as np

def apply_rotation(points: np.ndarray, alpha: float) -> np.ndarray:
    sin = np.sin(alpha)
    cos = np.cos(alpha)
    rotation_matrix = np.array([
        [cos, sin],
        [-sin, cos]
    ])
    return np.array([rotation_matrix @ p for p in points])
