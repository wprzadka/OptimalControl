from collections import namedtuple

CostWeights = namedtuple(
    'CostWeights', ['state_cost', 'control_cost', 'end_state_cost']
)
