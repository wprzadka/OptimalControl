import numpy as np


class InvertedPendulum:

    def __init__(self):
        # x[m], v[m/s], α[rad], ω[rad/s]
        self.state = np.array([0., 0., 0., 0.])
        self.A = np.array([
            # x, v, α, ω
            [0., 1., 0., 0.],  # x
            [0., 0., 0., 0.],  # v
            [0., 0., 0., 0.],  # α
            [0., 0., 0., 0.]   # ω
        ])
        self.B = np.array([[0.], [1.], [0.], [0.]])
        # a[m/s²]
        self.action_space = (-1., 1.)

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        state_derivative = self.A @ self.state + self.B @ action
        self.state += state_derivative * dt
        return self.state
