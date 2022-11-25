from simulation import Simulation
from physical_models.inverted_pendulum import InvertedPendulum

if __name__ == '__main__':

    pendulum = InvertedPendulum()
    sim = Simulation(pendulum)

    while sim.is_running:
        sim.update()
