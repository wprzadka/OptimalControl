import matplotlib.pyplot as plt
import numpy as np
import pygame as pg

from physical_models.physical_model_base import PhysicalModelBase
from utils.render_utils import apply_rotation


class TwoLinkArm(PhysicalModelBase):

    def __init__(self, angular_velocity: float):
        self.angular_velocity = angular_velocity
        self.lengths = np.array([100., 100.])

        #                      x1,   y1,   x2,   y2
        # self.state = np.array([100., 0., 200., 0.])

        angles = np.array([np.pi / 4, np.pi / 2])
        positions = self.compute_positions_from_angles(angles).flatten()
        print(angles, positions)
        self.hidden_state = np.concatenate((angles, positions))
        self._state = self.hidden_state[-2:]
        self.target = self.state + np.array([10., 0])

        self.action_space = np.array([[-1., 1.], [-1., 1.]])

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):

        self._state = value

    def set_target(self, target_state: np.ndarray):
        self.target = target_state

    def compute_positions_from_angles(self, angles: np.ndarray):
        l1, l2 = self.lengths
        th1, th2 = angles

        x1 = apply_rotation(np.array([[l1, 0]]), th1)[0]
        x2 = apply_rotation(np.array([[l2, 0]]), th1 + th2)[0] + x1
        return np.array([x1, x2])

    def f(self, action):
        l1, l2 = self.lengths
        th1, th2 = self.hidden_state[:2]

        derivatives = np.array([
            [-l1 * np.sin(th1) - l2 * np.sin(th1 + th2), -l2 * np.sin(th1 + th2)],
            [l1 * np.cos(th1) + l2 * np.cos(th1 + th2), l2 * np.cos(th1 + th2)]
        ])

        angles = self.hidden_state[:2] + self.angular_velocity * action
        self.hidden_state[:2] = (angles % (2*np.pi)) - np.where(angles < 0, 2 * np.pi, 0)
        self.hidden_state[2:] = self.compute_positions_from_angles(self.hidden_state[:2]).flatten()
        return derivatives @ action

    def render(self, window):
        center = np.array([300, 300])
        x1, x2 = self.compute_positions_from_angles(self.hidden_state[:2]) + center

        pg.draw.circle(window, (200, 20, 20), self.target + center, 4)

        pg.draw.line(window, (0, 160, 50), center, x1)
        pg.draw.line(window, (0, 160, 50), x1, x2)
        for point in [center, x1, x2]:
            pg.draw.circle(window, (100, 160, 50), point, 4)

    def get_input(self):
        pressed = pg.key.get_pressed()
        action = np.array([0, 0])

        # get movement speed
        if pressed[pg.K_q]:
            action[0] = 1.
        elif pressed[pg.K_a]:
            action[0] = -1.

        # get rotation speed
        if pressed[pg.K_w]:
            action[1] = 1.
        elif pressed[pg.K_s]:
            action[1] = -1.

        return action