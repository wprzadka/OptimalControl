import numpy as np

from physical_models.physical_model_base import PhysicalModelBase


class Seeker(PhysicalModelBase):

    def __init__(self):
        #                      x, y, \alpha
        self.state = np.array([0., 0., 0.])

        self.A_mat = np.array([
            # x y \alpha
            [0., 0., 0.],  # x
            [0., 0., 0.],  # y
            [0., 0., 0.]   # \alpha
        ])

        self.B_mat = np.array([
            # v, \omega
            [0., 0.],  # x
            [0., 0.],  # y
            [0., 1.]   # \alpha
        ])

        self.action_space = np.array([[-1., 1.], [-np.pi / 4, np.pi / 4]])

    def render(self, window):
        pass
