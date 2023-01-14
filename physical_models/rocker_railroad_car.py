import numpy as np
import pygame as pg

from physical_models.physical_model_base_linear import PhysicalModelBaseLinear


class RocketRailroadCar(PhysicalModelBaseLinear):

    def __init__(self, velocity):
        self.velocity = velocity
        self.state = np.array([100., 0.])
        self.target = np.zeros_like(self.state)

        self.A_mat = np.array([
            # x v
            [0., 1.],  # x
            [0., 0.]  # v
        ])
        self.B_mat = np.array([
            # a
            [0], # x
            [self.velocity]  # v
        ])
        self.action_space = np.array([[-1., 1.]])

    def set_target(self, target_state: np.ndarray):
        self.target = target_state

    def A(self):
        return self.A_mat

    def B(self):
        return self.B_mat

    def render(self, window):
        y = 200
        size = (50, 20)
        x, v = self.state
        center = np.array([x, y])

        body = pg.Rect(center - np.array([size[0] // 2, size[1] // 2]), size)
        pg.draw.rect(window, color=(50, 120, 50), rect=body)

        flame = center + np.sign(v) * np.array([[1, 0], [-1, -1], [-0.7, 0], [-1, 1]]) * 5
        pg.draw.polygon(window, color=(255, 20, 50), points=flame)

        pg.draw.circle(window, center=self.target + np.array([0, y]), radius=8, color=(0, 50, 160))

    def get_input(self):
        pressed = pg.key.get_pressed()
        action = np.array([0])

        # get rotation speed
        if pressed[pg.K_LEFT]:
            action[0] = -1.
        elif pressed[pg.K_RIGHT]:
            action[0] = 1.

        return action
