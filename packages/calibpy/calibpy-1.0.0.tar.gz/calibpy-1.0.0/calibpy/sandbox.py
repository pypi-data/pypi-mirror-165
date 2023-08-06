import numpy as np

vec = np.array([[1, 0], [0, 1], [1, 1], [-1, -1]])
T = np.array([[-1, 1], [0, 1]])

print(np.dot(vec, T))
