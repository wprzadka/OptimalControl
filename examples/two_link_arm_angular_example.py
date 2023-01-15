import numpy as np

from control_algorithms.costs_weights import CostWeights
from control_algorithms.linear_quadratic_regulator import LinearQuadraticRegulator
from physical_models.two_link_arm_angular import TwoLinkArmIk
from simulation import Simulation

if __name__ == '__main__':

    torque = 1 / np.pi
    model = TwoLinkArmIk(torque=torque)
    state_cost = np.array([
        [1, 0 , 0, 0],
        [ 0, 1, 0, 0],
        [ 0,  0, 0, 0],
        [ 0,  0, 0, 0]
    ])
    end_state_cost = np.array([
        [10,  0,  0,  0],
        [ 0, 10,  0,  0],
        [ 0,  0, 100,  0],
        [ 0,  0,  0, 100]
    ])
    control_cost = np.array([
        [10, 0],
        [0, 10]
    ])


    control = LinearQuadraticRegulator(
        model=model,
        cost_weights=CostWeights(state_cost=state_cost, control_cost=control_cost, end_state_cost=end_state_cost),
        time_horizon=10
    )
    control.set_target(np.array([np.pi / 4, np.pi / 2, 0, 0]))
    model.action_space *= torque
    # MANUAL CONTROL
    # control = None

    sim = Simulation(model, control_model=control, delta_time=0.1)

    while sim.is_running:
        sim.update()
