import numpy as np
import matplotlib.pyplot as plt

# Generating the circuit
def generate_circuit():
    circuit_matrix = np.genfromtxt('robot_positions.csv', delimiter=',')
    plt.scatter(*zip(*circuit_matrix[1:]))
    plt.plot(*zip(*circuit_matrix[1:]))
    plt.show()

generate_circuit()