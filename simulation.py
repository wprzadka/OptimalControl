import numpy as np
import pygame as pg


class Simulation:

    def __init__(self, physical_model):
        self.RESOLUTION = (640, 480)
        self.BACKGROUND = (20, 40, 60)

        self.is_running = True
        self.delta_time = 0.1
        self.physical_model = physical_model

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

        self.read_input()

    def read_input(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
            elif event.type == pg.QUIT:
                self.is_running = False

        action = self.physical_model.get_input()

        self.physical_model.update(action, self.delta_time)
