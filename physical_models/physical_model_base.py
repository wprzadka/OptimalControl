import abc
import numpy as np


class PhysicalModelBase(abc.ABC):

    state = None
    action_space = None

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        state_derivative = self.f(action)
        self.state += state_derivative * dt
        return self.state

    @abc.abstractmethod
    def f(self, action):
        pass

    @abc.abstractmethod
    def render(self, window):
        pass

    @abc.abstractmethod
    def get_input(self) -> np.ndarray:
        pass

    @abc.abstractmethod
    def set_target(self, target_state: np.ndarray):
        pass
