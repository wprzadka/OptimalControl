from typing import Union

import numpy as np

class PID:

    def __init__(
            self,
            state_dim: int,
            weights_p: Union[float, np.ndarray],
            weights_i: Union[float, np.ndarray],
            weights_d: Union[float, np.ndarray]
    ):
        self.w_p = weights_p # proportional term
        self.w_i = weights_i # integral term
        self.w_d = weights_d # derivative term
        self.target = np.zeros(state_dim)

        self.last_error = np.zeros(state_dim)
        self.integrated_error = np.zeros(state_dim)

    def set_target(self, target_state: np.ndarray):
        self.target = target_state

    def __call__(self, state: np.ndarray, dt: float):
        return self.compute_feedback(state, dt)

    def compute_feedback(self, state: np.ndarray, dt: float):
        error = self.target - state
        self.integrated_error += error * dt

        p = error
        i = self.integrated_error
        d = (error - self.last_error) / dt

        self.last_error = error
        return self.w_p * p + self.w_i * i + self.w_d * d
