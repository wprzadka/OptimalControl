import pygame as pg
from simulation import Simulation
from inverted_pendulum import InvertedPendulum

if __name__ == '__main__':

    pendulum = InvertedPendulum()
    sim = Simulation(pendulum)

    while sim.is_running:
        sim.update()
