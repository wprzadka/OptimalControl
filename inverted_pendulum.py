import numpy as np
import pygame as pg


class InvertedPendulum:

    def __init__(self):
        self.length = 100.
        self.y_pos = 200.

        # x[m], v[m/s], α[rad], ω[rad/s]
        self.state = np.array([0., 0., 0., 0.])
        self.A = np.array([
            # x, v, α, ω
            [0., 1., 0., 0.],  # x
            [0., 0., 0., 0.],  # v
            [0., 0., 0., 0.],  # α
            [0., 0., 0., 0.]   # ω
        ])
        self.B = np.array([[0.], [1.], [0.], [0.]])
        # a[m/s²]
        self.action_space = (-1., 1.)

    def update(self, action: np.ndarray, dt: float) -> np.ndarray:
        state_derivative = self.A @ self.state + self.B @ action
        self.state += state_derivative * dt
        return self.state

    def render(self, window):
        body_width, body_high = 100, 50

        x, alpha = self.state[[0, 2]]
        print(x, alpha)
        body = pg.Rect(x - body_width / 2, self.y_pos - body_high / 2, body_width, body_high)
        pg.draw.rect(window, color=(0, 120, 255), rect=body)

        pos = np.array([x, self.y_pos])
        end_pos = np.array([x, self.y_pos]) + np.array([np.sin(alpha), np.cos(alpha)]) * self.length
        pg.draw.line(window, color=(120, 50, 50), start_pos=pos, end_pos=end_pos)
        pg.draw.circle(window, color=(0, 120, 255), center=end_pos, radius=4)