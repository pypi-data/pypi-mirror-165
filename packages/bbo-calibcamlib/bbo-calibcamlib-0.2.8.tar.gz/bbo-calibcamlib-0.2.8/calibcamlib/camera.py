import numpy as np
from .dist_MaEtAl2003_model0 import distort, distort_inverse  # TODO: make model variable


class Camera:
    def __init__(self, A, k, offset=None, distortion=None):  # TODO: Implement variable distortion
        if offset is None:
            offset = [0, 0]

        self.offset = offset
        self.A = A.reshape(3, 3)
        self.k = k.reshape(5)

    def space_to_sensor(self, X, offset=None):
        if offset is None:
            offset = self.offset

        assert self.k[2] == 0 and self.k[3] == 0 and self.k[4] == 0

        # code from calibcam.multical_plot.project_board
        x = X / X[:, 2, np.newaxis]

        x[:, 0:2] = distort(x[:, 0:2], self.k)

        x = x @ self.A.T

        return x[:, 0:2] - offset

    def sensor_to_space(self, x, offset=None):
        if offset is None:
            offset = self.offset

        # assert self.k[2] == 0 and self.k[3] == 0 and self.k[4] == 0
        x = x + offset

        X = np.zeros(shape=(x.shape[0], 3))
        X[:, 0:2] = x
        X[:, 2] = 1

        X = X @ np.linalg.inv(self.A.T)

        X[:, 0:2] = distort_inverse(X[:, 0:2], self.k)

        X /= np.sqrt(np.sum(X ** 2, axis=1))[:, np.newaxis]

        return X
