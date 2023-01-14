import numpy as np

from control_algorithms.costs_weights import CostWeights
from control_algorithms.linear_quadratic_regulator import LinearQuadraticRegulator
from physical_models.rocker_railroad_car import RocketRailroadCar
from simulation import Simulation

if __name__ == '__main__':

    model = RocketRailroadCar(velocity=1.)
    state_cost = np.array([
        [100, 0],
        [0, 0.01]
    ])
    end_state_cost = np.array([
        [100, 0],
        [0, 100]
    ])
    control_cost = np.array([[10]])

    control = LinearQuadraticRegulator(
        model=model,
        cost_weights=CostWeights(state_cost=state_cost, control_cost=control_cost, end_state_cost=end_state_cost),
        time_horizon=1000
    )

    model.state = np.array([100., 0.])
    control.set_target(np.array([500., 0.]))
    model.action_space *= 100
    # control = None

    sim = Simulation(model, control_model=control)

    while sim.is_running:
        sim.update()