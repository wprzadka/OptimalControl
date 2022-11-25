import numpy as np
import pygame as pg

from physical_models.physical_model_base import PhysicalModelBase


class InvertedPendulum(PhysicalModelBase):

    def __init__(self):
        self.length = 100.
        self.y_pos = 200.
        self.gravity = 9.81
        self.m_card = 2.5
        self.m_pendulum = 0.2

        # x[m], v[m/s], α[rad], ω[rad/s]
        self.state = np.array([200., 0., 0., 0.])

        h1 = -self.m_pendulum * self.gravity / self.m_card
        h2 = (self.m_card + self.m_pendulum) * self.gravity / (self.m_card * self.length)
        self.A_mat = np.array([
            # x, v, α, ω
            [0., 1., 0., 0.],  # x
            [0., 0., h1, 0.],  # v
            [0., 0., 0., 1.],  # α
            [0., 0., h2, 0.]   # ω
        ])
        self.B_mat = np.array([[0.], [1. / self.m_card], [0.], [1. / (self.m_card * self.length)]])
        # a[m/s²]
        self.action_space = np.array([[-1., 1.]])

        # self.body_definition = {
        #     0: (100, 50),
        #     2: (5)
        # }

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        # state_derivative = self.A() @ self.state + self.B() @ action
        state_derivative = self.A_mat @ self.state + self.B_mat @ action
        # state_derivative = self.f(action[0])
        self.state += state_derivative * dt
        return self.state

    def A(self):
        x, v, alpha, omega = self.state
        b = self.get_pendulum_side(alpha)
        h1 = b * self.m_pendulum * self.gravity / self.m_card
        h2 = -b * (self.m_card + self.m_pendulum) * self.gravity / (self.m_card * self.length)
        A = np.array([
            # x, v, α, ω
            [0., 1., 0., 0.],  # x
            [0., 0., h1, 0.],  # v
            [0., 0., 0., 1.],  # α
            [0., 0., h2, 0.]  # ω
        ])
        return A

    def B(self):
        x, v, alpha, omega = self.state
        b = self.get_pendulum_side(alpha)

        B = np.array([
            [0.],
            [1. / self.m_card],
            [0.],
            [b / (self.m_card * self.length)]
        ])
        return B

    def get_pendulum_side(self, alpha: float) -> int:
        return 1 if np.abs(alpha) > np.pi / 2 else -1

    # def f(self, action: float):
    #     # x[m], v[m/s], α[rad], ω[rad/s]
    #     x, v, alpha, d_alpha = self.state
    #     theta = np.pi - alpha
    #     omega = -d_alpha
    #     m = self.m_pendulum
    #     M = self.m_card
    #     g = self.gravity
    #     length = self.length
    #     dumping = 0
    #
    #     dv = ((-m ** 2 * length ** 2 * g * np.cos(theta) * np.sin(theta)
    #            + m * length ** 2 * (m * length * omega ** 2 * np.sin(theta) - dumping * v)
    #            + m * length ** 2 * action
    #            )
    #           / (m * length ** 2 * (M + m * (1 - np.cos(theta) ** 2)))
    #           )
    #     d_omega = ((m + M) * m * g * length * np.sin(theta)
    #                - m * length * np.cos(theta) * (m * length * omega ** 2 * np.sin(theta) - dumping * v)
    #                + m * length * np.cos(theta) * action
    #                / (m * length ** 2 * (M + m * (1 - np.cos(theta) ** 2))))
    #     return np.array([v, dv, omega, d_omega])

    def render(self, window):
        body_width, body_high = 100, 50

        x, alpha = self.state[[0, 2]]
        body = pg.Rect(x - body_width / 2, self.y_pos - body_high / 2, body_width, body_high)
        pg.draw.rect(window, color=(0, 120, 255), rect=body)

        pos = np.array([x, self.y_pos])
        end_pos = np.array([x, self.y_pos]) + np.array([np.sin(alpha), np.cos(alpha)]) * self.length
        pg.draw.line(window, color=(120, 50, 50), start_pos=pos, end_pos=end_pos)
        pg.draw.circle(window, color=(0, 120, 255), center=end_pos, radius=4)
