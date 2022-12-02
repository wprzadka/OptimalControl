import numpy as np

from control_algoriithms.costs_weights import CostWeights
from control_algoriithms.linear_quadratic_regulator import LinearQuadraticRegulator
from control_algoriithms.pid import PID
from physical_models.rocker_railroad_car import RocketRailroadCar
from simulation import Simulation
from physical_models.inverted_pendulum import InvertedPendulum
from physical_models.seeker import Seeker

if __name__ == '__main__':

    # model = InvertedPendulum()
    model = Seeker(velocity=50.)
    # model = RocketRailroadCar(velocity=50.)

    control = None
    # control = PID(model.state.shape[0], 1, 0, 0)
    # control = LinearQuadraticRegulator(model=model, cost_weights=CostWeights(1, 1, 0), time_horizon=2)

    sim = Simulation(model, control)

    while sim.is_running:
        sim.update()
