import abc
import numpy as np

from physical_models.physical_model_base import PhysicalModelBase


class PhysicalModelBaseLinear(PhysicalModelBase):

    def f(self, action: np.ndarray):
        return self.A() @ self.state + self.B() @ action

    @abc.abstractmethod
    def A(self) -> np.ndarray:
        pass

    @abc.abstractmethod
    def B(self) -> np.ndarray:
        pass
