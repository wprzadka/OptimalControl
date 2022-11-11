import numpy as np
import pygame as pg


class Simulation:

    def __init__(self, pendulum):
        self.RESOLUTION = (640, 480)
        self.BACKGROUND = (20, 40, 60)

        self.is_running = True
        self.delta_time = 1.
        self.pendulum = pendulum

        pg.init()
        self.window = pg.display.set_mode(self.RESOLUTION)
        self.clock = pg.time.Clock()

    def update(self):
        self.clock.tick(30)

        self.window.fill(self.BACKGROUND)
        # x, v, alpha, w = self.pendulum.state
        # pg.draw.rect(self.window, (255, 128, 255), pg.Rect(x, 100, 60, 60))
        self.pendulum.render(self.window)
        pg.display.update()

        self.read_input()

    def read_input(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
            elif event.type == pg.QUIT:
                self.is_running = False

        # provide inputs for pendulum
        pressed = pg.key.get_pressed()
        action = np.array([0])
        if pressed[pg.K_LEFT]:
            action = np.array([-1.])
        elif pressed[pg.K_RIGHT]:
            action = np.array([1.])

        self.pendulum.update(action, self.delta_time)
