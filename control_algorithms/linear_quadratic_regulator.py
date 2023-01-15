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
            time_horizon: float,
            delta_time: float = 0.1
    ):
        self.is_linear = isinstance(model, PhysicalModelBaseLinear)

        self.model = model
        self.time_horizon = time_horizon
        self.dt = delta_time

        self.cost_weights = cost_weights
        self.target_state = np.zeros_like(model.state)

        self.state_cost = cost_weights.state_cost
        self.control_cost = cost_weights.control_cost
        self.end_state_cost = cost_weights.end_state_cost

    def __call__(self, state: np.ndarray):
        return self.compute_action(state)

    def set_target(self, target_state: np.ndarray):
        self.model.set_target(target_state)
        self.target_state = target_state

    def compute_action(self, state: np.ndarray):
        K_vals, action = self.compute_riccati() if self.is_linear else self.compute_riccati_nonlinear(state)
        action = np.clip(action, self.model.action_space[:, 0], self.model.action_space[:, 1])
        return action

    def compute_riccati(self):
        assert isinstance(self.model, PhysicalModelBaseLinear)

        K_vals = np.empty(shape=(int(np.ceil(self.time_horizon / self.dt)), *self.end_state_cost.shape))
        K_vals[-1] = -self.end_state_cost
        B = self.model.B()
        A = self.model.A()
        inv_control_cost = np.linalg.inv(self.control_cost)

        for t in range(len(K_vals) - 1, 0, -1):
            K_vals[t - 1] = K_vals[t] + self.dt * (
                    K_vals[t] @ B @ inv_control_cost @ B.T @ K_vals[t]
                    + K_vals[t] @ A
                    + A.T @ K_vals[t]
                    - self.state_cost
            )
        u_star = inv_control_cost @ self.model.B().T @ K_vals[0] @ (self.model.state - self.target_state)
        return K_vals, u_star

    def compute_linearized_A(self, model, action, dx, dt):
        A = np.empty(shape=(model.state.shape[0], model.state.shape[0]))

        for idx, _ in enumerate(model.state):
            model_copy = deepcopy(model)
            model_copy.state[idx] += dx
            forward = model.state + model_copy.f(action) * dt

            model_copy = deepcopy(model)
            model_copy.state[idx] -= dx
            backward = model.state + model_copy.f(action) * dt

            A[:, idx] = (forward - backward) / (2 * dx)
        return A

    def compute_linearized_B(self, model, action, du, dt):
        B = np.empty(shape=(model.state.shape[0], action.shape[0]))
        for idx, _ in enumerate(action):
            model_copy = deepcopy(model)
            action_copy = action.copy()
            action_copy[idx] += du
            forward = model.state + model_copy.f(action_copy) * dt

            model_copy = deepcopy(model)
            action_copy = action.copy()
            action_copy[idx] -= du
            backward = model.state + model_copy.f(action_copy) * dt

            B[:, idx] = (forward - backward) / (2 * du)
        return B

    def compute_riccati_nonlinear(self, state: np.ndarray):
        K_vals = np.empty(shape=(int(np.ceil(self.time_horizon / self.dt)), *self.end_state_cost.shape))
        K_vals[-1] = -self.end_state_cost
        inv_control_cost = np.linalg.inv(self.control_cost)

        model = deepcopy(self.model)
        u_star = np.zeros(model.action_space.shape[0])
        A = self.compute_linearized_A(model, u_star, 0.00001, self.dt)
        B = self.compute_linearized_B(model, u_star, 0.00001, self.dt)

        for t in range(len(K_vals) - 1, 0, -1):
            # A = self.compute_linearized_A(model, u_star, 0.1, self.dt)
            # B = self.compute_linearized_B(model, u_star, 0.1, self.dt)
            # u_star = inv_control_cost @ B.T @ K_vals[t] @ (state - self.target_state)

            K_vals[t - 1] = K_vals[t] + self.dt * (
                    K_vals[t] @ B @ inv_control_cost @ B.T @ K_vals[t]
                    + K_vals[t] @ A
                    + A.T @ K_vals[t]
                    - self.state_cost
            )
        u_star = inv_control_cost @ B.T @ K_vals[0] @ (state - self.target_state)
        return K_vals, u_star
