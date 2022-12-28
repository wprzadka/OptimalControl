import numpy as np
from copy import deepcopy

from physical_models.physical_model_base import PhysicalModelBase
from physical_models.physical_model_base_linear import PhysicalModelBaseLinear
from .costs_weights import CostWeights


class LinearQuadraticRegulator:

    def __init__(
            self,
            model: PhysicalModelBase,
            cost_weights: CostWeights,
            time_horizon: float
    ):
        self.is_linear = isinstance(model, PhysicalModelBaseLinear)

        if not self.is_linear:
            raise NotImplementedError('LQR for non linear systems is not implemented yet')

        self.model = model
        self.time_horizon = time_horizon

        self.cost_weights = cost_weights
        self.target_state = np.zeros_like(model.state)
        self.state_cost = cost_weights.state_cost * np.eye(model.state.shape[0])
        self.control_cost = cost_weights.control_cost * np.eye(model.action_space.shape[0])
        # self.control_cost = np.diag(np.full_like(model.state, fill_value=cost_weights.control_cost))
        self.end_state_cost = cost_weights.end_state_cost * np.eye(model.state.shape[0])
        # self.end_state_cost = np.diag(np.full_like(model.state, fill_value=cost_weights.end_state_cost))

    def __call__(self, state: np.ndarray, dt: float):
        return self.compute_action(state, dt)

    def set_target(self, target_state: np.ndarray):
        self.model.set_target(target_state)
        self.target_state = target_state

    def compute_action(self, state:np.ndarray, dt: float):
        K_vals = self.compute_riccati(dt)

        inv_control_cost = np.linalg.inv(self.control_cost)
        u_star = inv_control_cost @ self.model.B().T @ K_vals[0] @ (state - self.target_state)
        return u_star

    def compute_riccati(self, dt: float):
        assert isinstance(self.model, PhysicalModelBaseLinear)

        K_vals = np.empty(shape=(int(np.ceil(self.time_horizon / dt)), *self.end_state_cost.shape))
        K_vals[-1] = -self.end_state_cost
        B = self.model.B()
        A = self.model.A()
        inv_control_cost = np.linalg.inv(self.control_cost)

        for t in range(len(K_vals) - 1, 0, -1):
            K_vals[t - 1] = K_vals[t] + dt * (
                    K_vals[t] @ B @ inv_control_cost @ B.T @ K_vals[t]
                    + K_vals[t] @ A
                    + A.T @ K_vals[t]
                    - self.state_cost
            )
        return K_vals
