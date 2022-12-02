import numpy as np

from control_algorithms.costs_weights import CostWeights
from control_algorithms.linear_quadratic_regulator import LinearQuadraticRegulator
from control_algorithms.pid import PID
from physical_models.rocker_railroad_car import RocketRailroadCar
from simulation import Simulation
from physical_models.inverted_pendulum import InvertedPendulum
from physical_models.seeker import Seeker

if __name__ == '__main__':

    # model = InvertedPendulum()
    # model = Seeker(velocity=50.)
    model = RocketRailroadCar(velocity=1.)

    # control = None
    # control = PID(model.state.shape[0], 1, 0, 0)
    control = LinearQuadraticRegulator(model=model, cost_weights=CostWeights(1, 1, 0), time_horizon=0.5)
    control.set_target(np.array([500, 0]))

    sim = Simulation(model, control)

    while sim.is_running:
        sim.update()
