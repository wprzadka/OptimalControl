import numpy as np
import pygame as pg

from physical_models.physical_model_base import PhysicalModelBase


class Simulation:

    def __init__(self, physical_model: PhysicalModelBase, control_model = None, delta_time: float = 0.1):
        self.RESOLUTION = (640, 480)
        self.BACKGROUND = (20, 40, 60)

        self.is_running = True
        self.delta_time = delta_time
        self.physical_model = physical_model

        self.control = control_model

        pg.init()
        self.window = pg.display.set_mode(self.RESOLUTION)
        self.clock = pg.time.Clock()

    def update(self):
        self.clock.tick(30)

        self.window.fill(self.BACKGROUND)
        # x, v, alpha, w = self.pendulum.state
        # pg.draw.rect(self.window, (255, 128, 255), pg.Rect(x, 100, 60, 60))
        self.physical_model.render(self.window)
        pg.display.update()

        if self.control is None:
            action = self.read_input()
        else:
            action = self.control(self.physical_model.state)

        self.physical_model.update(action, self.delta_time)


    def read_input(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
            elif event.type == pg.QUIT:
                self.is_running = False
        action = self.physical_model.get_input()
        return action
