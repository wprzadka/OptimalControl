import numpy as np


class PhysicalModelBase:

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        pass

    def render(self, window):
        pass
