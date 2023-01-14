import numpy as np

from control_algorithms.costs_weights import CostWeights
from control_algorithms.linear_quadratic_regulator import LinearQuadraticRegulator
from physical_models.two_link_arm import TwoLinkArm
from simulation import Simulation

if __name__ == '__main__':

    angular_velocity = 0.1 / np.pi
    model = TwoLinkArm(angular_velocity=angular_velocity)
    state_cost = np.array([
        [10, 0],
        [0, 10]
    ])
    end_state_cost = np.array([
        [10, 0],
        [0, 10]
    ])
    control_cost = np.array([
        [10, 0],
        [0, 10]
    ])

    control = LinearQuadraticRegulator(
        model=model,
        cost_weights=CostWeights(state_cost=state_cost, control_cost=control_cost, end_state_cost=end_state_cost),
        time_horizon=1000
    )
    model.action_space *= angular_velocity
    # MANUAL CONTROL
    control = None

    sim = Simulation(model, control_model=control)

    while sim.is_running:
        sim.update()
