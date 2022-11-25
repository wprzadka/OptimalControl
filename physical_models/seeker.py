import numpy as np
import pygame as pg

from physical_models.physical_model_base import PhysicalModelBase


class Seeker(PhysicalModelBase):

    def __init__(self):
        #                      x, y, \alpha
        self.state = np.array([200., 200., 0.])

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

    def apply_rotation(self, points: np.ndarray, alpha: float) -> np.ndarray:
        sin = np.sin(alpha)
        cos = np.cos(alpha)
        rotation_matrix = np.array([
            [cos, sin],
            [-sin, cos]
        ])
        return np.array([rotation_matrix @ p for p in points])

    def render(self, window):
        points = np.array([[0, 1], [-1, -1], [0, -0.7], [1, -1]]) * 20
        x, y, alpha = self.state

        center = np.array([x, y])
        points = center + self.apply_rotation(points, alpha)
        pg.draw.polygon(window, color=(50, 120, 50), points=points)

    def get_input(self):
        pressed = pg.key.get_pressed()
        action = np.array([0, 0])

        # get movement speed
        if pressed[pg.K_UP]:
            action[0] = 1.
        elif pressed[pg.K_DOWN]:
            action[0] = -1.

        # get rotation speed
        if pressed[pg.K_LEFT]:
            action[1] = -1.
        elif pressed[pg.K_RIGHT]:
            action[1] = 1.

        return action
