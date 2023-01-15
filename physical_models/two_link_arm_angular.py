import matplotlib.pyplot as plt
import numpy as np
import pygame as pg

from physical_models.physical_model_base_linear import PhysicalModelBaseLinear
from utils.render_utils import apply_rotation


class TwoLinkArmIk(PhysicalModelBaseLinear):

    def __init__(self, torque: float, arms_lengths: np.ndarray = None):
        self.torque = torque
        self.lengths = arms_lengths or np.array([50., 50.])

        self.state = np.array([np.pi / 2, -np.pi / 2, 0, 0])
        self.target = np.array([np.pi / 4, np.pi / 4, 0, 0])
        self.target_position = self.compute_positions_from_angles(self.target[:2])[1]
        self.action_space = np.array([[-1., 1.], [-1., 1.]])

    def set_target(self, target_state: np.ndarray):
        self.target = target_state
        self.target_position = self.compute_positions_from_angles(self.target[:2])[-1]

    def compute_desired_angles_with_inverse_kinematics(self, desired_position):
        x, y = desired_position
        l1, l2 = self.lengths
        q2 = np.arccos((x**2 + y**2 - l1**2 - l2**2) / 2 * l1 * l2)
        q1 = np.arctan(y / x) - np.arctan(l2 * np.sin(q2) / (l1 + l2 * np.cos(q2)))
        return np.array([q1, q2])

    def compute_positions_from_angles(self, angles: np.ndarray):
        l1, l2 = self.lengths
        th1, th2 = angles
        x1 = apply_rotation(np.array([[l1, 0]]), th1)[0]
        x2 = apply_rotation(np.array([[l2, 0]]), th1 + th2)[0] + x1
        return np.array([x1, x2])

    def A(self):
        return np.array([
        #    θ1 θ2 ω1 ω2
            [0, 0, 1, 0], # θ1
            [0, 0, 0, 1], # θ2
            [0, 0, 0, 0], # ω1
            [0, 0, 0, 0]  # ω2
        ])

    def B(self):
        return np.array([
        #   τ1  τ2
            [0, 0], # θ1
            [0, 0],  # θ2
            [1, 0],  # ω1
            [0, 1]  # ω2
        ])

    def render(self, window):
        center = np.array([300, 300])
        print(self.target_position)
        pg.draw.circle(window, (200, 20, 20), self.target_position + center, 4)
        x1, x2 = self.compute_positions_from_angles(self.state[:2]) + center
        pg.draw.line(window, (0, 160, 50), center, x1)
        pg.draw.line(window, (0, 160, 50), x1, x2)
        for point in [center, x1, x2]:
            pg.draw.circle(window, (100, 160, 50), point, 4)

    def get_input(self):
        pressed = pg.key.get_pressed()
        action = np.array([0, 0])

        # 1st motor torque
        if pressed[pg.K_q]:
            action[0] = 1.
        elif pressed[pg.K_a]:
            action[0] = -1.

        # 2nd motor torque
        if pressed[pg.K_w]:
            action[1] = 1.
        elif pressed[pg.K_s]:
            action[1] = -1.

        return action