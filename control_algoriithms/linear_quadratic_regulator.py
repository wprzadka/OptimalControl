import numpy as np

from physical_models.physical_model_base import PhysicalModelBase
from .costs_weights import CostWeights


class LinearQuadraticRegulator:

    def __init__(self, model: PhysicalModelBase, cost_weights: CostWeights, time_horizon: int):

        self.model = model
        self.time_horizon = time_horizon

        self.target_state = np.zeros_like(model.state)
        self.state_cost = cost_weights.state_cost * np.eye(model.state.shape[0])
        self.control_cost = cost_weights.control_cost * np.eye(model.state.shape[0])
        # self.control_cost = np.diag(np.full_like(model.state, fill_value=cost_weights.control_cost))
        self.end_state_cost = cost_weights.end_state_cost * np.eye(model.state.shape[0])
        # self.end_state_cost = np.diag(np.full_like(model.state, fill_value=cost_weights.end_state_cost))

    def __call__(self, state: np.ndarray, dt: float):
        return self.compute_action(state, dt)

    def set_target(self, target_state: np.ndarray):
        self.target_state = target_state

    def compute_action(self, state:np.ndarray, dt: float):
        K_vals = self.compute_riccati(dt)
        print([i for i, v in enumerate(K_vals) if not np.any(np.isnan(v))])

        # for t, k_val in enumerate(K_vals):
        #     u

        u_star = self.model.B().T @ K_vals[0] @ state
        print(u_star)
        return u_star

    def compute_riccati(self, dt: float):
        K_vals = np.empty(shape=(int(np.ceil(self.time_horizon / dt)), *self.end_state_cost.shape))
        K_vals[-1] = -self.end_state_cost
        B = self.model.B()

        for t in range(len(K_vals) - 1, 0, -1):
            K_vals[t - 1] = K_vals[t] + dt * (K_vals[t] @ B @ B.T @ K_vals[t] + self.state_cost)
        return K_vals