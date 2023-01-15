import numpy as np

from control_algorithms.costs_weights import CostWeights
from control_algorithms.linear_quadratic_regulator import LinearQuadraticRegulator
from physical_models.seeker import Seeker
from simulation import Simulation

if __name__ == '__main__':

    velocity = 2.5
    angular_velocity = 1. / np.pi
    model = Seeker(velocity=velocity, angular_velocity=angular_velocity)
    state_cost = np.array([
        [10, 0, 0],
        [0, 10, 0],
        [0, 0, 0.01]
    ])
    end_state_cost = np.array([
        [10, 0, 0],
        [0, 10, 0],
        [0, 0, 100]
    ])
    control_cost = np.array([
        [10, 0],
        [0, 10]
    ])

    control = LinearQuadraticRegulator(
        model=model,
        cost_weights=CostWeights(state_cost=state_cost, control_cost=control_cost, end_state_cost=end_state_cost),
        time_horizon=100
    )

    control.set_target(np.array([300., 300., np.pi]))
    model.action_space[0] *= velocity
    model.action_space[1] *= angular_velocity
    # control = None

    sim = Simulation(model, control_model=control)

    while sim.is_running:
        sim.update()