import numpy as np


class PhysicalModelBase:

    state = None

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        state_derivative = self.A() @ self.state + self.B() @ action
        self.state += state_derivative * dt
        return self.state

    def render(self, window):
        pass

    def get_input(self) -> np.ndarray:
        pass

    def A(self) -> np.ndarray:
        pass

    def B(self) -> np.ndarray:
        pass
