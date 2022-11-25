import numpy as np


class PhysicalModelBase:

    state = None
    A_mat = None
    B_mat = None

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        state_derivative = self.A_mat @ self.state + self.B_mat @ action
        self.state += state_derivative * dt
        return self.state

    def render(self, window):
        pass
