import matplotlib.pyplot as plt
import numpy as np
import pygame as pg

from physical_models.physical_model_base import PhysicalModelBase
from utils.render_utils import apply_rotation


class TwoLinkArm(PhysicalModelBase):

    def __init__(self, angular_velocity: float, arms_lengths: np.ndarray = None):
        self.angular_velocity = angular_velocity
        self.lengths = arms_lengths or np.array([50., 50.])

        angles = np.array([np.pi / 4, -np.pi / 4])
        self.state = self.compute_positions_from_angles(angles).flatten()
        target_angles = np.array([np.pi / 8, np.pi / 2])
        self.target = self.compute_positions_from_angles(target_angles).flatten()

        self.action_space = np.array([[-1., 1.], [-1., 1.]])

    def set_target(self, target_state: np.ndarray):
        self.target = target_state

    def compute_positions_from_angles(self, angles: np.ndarray):
        l1, l2 = self.lengths
        th1, th2 = angles

        x1 = apply_rotation(np.array([[l1, 0]]), th1)[0]
        x2 = apply_rotation(np.array([[l2, 0]]), th1 + th2)[0] + x1
        return np.array([x1, x2])

    def compute_angles_from_positions(self, positions: np.ndarray):
        x1, x2 = positions
        diff = x2 - x1
        th1 = np.arctan2(x1[1], x1[0])
        th2 = np.arctan2(diff[1], diff[0]) - th1
        return np.array([th1, th2])

    def f(self, action):
        l1, l2 = self.lengths
        th1, th2 = self.compute_angles_from_positions(self.state.reshape(-1, 2))

        derivatives = np.array([
            [-l1 * np.sin(th1), 0],
            [l1 * np.cos(th1), 0],
            [-l1 * np.sin(th1) - l2 * np.sin(th1 + th2), -l2 * np.sin(th1 + th2)],
            [l1 * np.cos(th1) + l2 * np.cos(th1 + th2), l2 * np.cos(th1 + th2)]
        ])
        return derivatives @ action

    def render(self, window):
        center = np.array([300, 300])
        x1 = self.state[:2] + center
        x2 = self.state[2:] + center

        pg.draw.circle(window, (200, 20, 20), self.target[2:] + center, 4)
        pg.draw.line(window, (0, 160, 50), center, x1)
        pg.draw.line(window, (0, 160, 50), x1, x2)
        for point in [center, x1, x2]:
            pg.draw.circle(window, (100, 160, 50), point, 4)

    def get_input(self):
        pressed = pg.key.get_pressed()
        action = np.array([0, 0])

        # 1st motor rotation speed
        if pressed[pg.K_q]:
            action[0] = 1.
        elif pressed[pg.K_a]:
            action[0] = -1.

        # 2nd motor rotation speed
        if pressed[pg.K_w]:
            action[1] = 1.
        elif pressed[pg.K_s]:
            action[1] = -1.

        return action