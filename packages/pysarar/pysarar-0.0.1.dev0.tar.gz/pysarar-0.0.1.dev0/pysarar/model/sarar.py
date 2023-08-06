from locale import normalize
import numpy as np
from typing import List


class SARAR:
    """An implementation of the two-step TSLS-GMM estimator proposed by Badinger and Egger (2010) for higher-order spatial autoregressive cross-section models with heteroscedastic disturbances."""

    def __init__(self, Q: int, num_instruments: int) -> None:
        """Instantiate a SARAR model

        :param Q: Weight matrix powers considered in instrument generation.
        :type Q: int
        :param num_instruments: Number of instruments to be used in the two stage least squares estimation.
        :type num_instruments: int
        """
        self.Q = Q
        self.num_instuments = num_instruments

    def fit(
        self, y: np.ndarray, X: np.ndarray, W: List[np.ndarray], M: List[np.ndarray]
    ) -> None:
        """Fit a SARAR(R, S) model

        :param y: Vector of observed outcomes
        :type y: np.ndarray
        :param X: Matrix of exogenous covariates
        :type X: np.ndarray
        :param W: List of weight matrices
        :type W: List[np.ndarray]
        :param M: List of disturbance weight matrices
        :type M: List[np.ndarray]
        """
        self.y = y
        self.X = X
        self.W = W
        self.M = M

        # Assert y is one dimensional
        assert self.y.ndim == 1

        # Generate number of observations
        self.N = len(self.y)

        # Assert dimensionalities of inputs
        assert all(
            [weight_matrix.ndim == 2 for weight_matrix in self.W]
        ), "Dimension mismatch: weight matrix must be a 2 dimensional array."
        assert all(
            [weight_matrix.ndim == 2 for weight_matrix in self.M]
        ), "Dimension mismatch: weight matrix must be a 2 dimensional array."
        assert all(
            [weight_matrix.shape == (self.N, self.N) for weight_matrix in self.W]
        ), "Dimension mismatch: weight matrix size must match number of observations."
        assert all(
            [weight_matrix.shape == (self.N, self.N) for weight_matrix in self.M]
        ), "Dimension mismatch: weight matrix size must match number of observations."
        assert (
            X.shape[0] == self.N
        ), "Dimension mismatch: feature matrix size must match number of observations"
        self.delta = self._TSLS()

    def _TSLS(self) -> np.ndarray:
        """Perform a two stage least squares estimation

        :return: parameter estimates
        :rtype: np.ndarray
        """
        Y_bar = np.concatenate(
            [
                np.expand_dims(np.dot(weight_matrix, self.y), axis=1)
                for weight_matrix in self.W
            ],
            axis=1,
        )
        sum_W = sum(self.W)
        instruments = np.dot(
            sum([np.linalg.matrix_power(sum_W, i + 1) for i in range(self.Q)]), self.X
        )
        H_N = np.concatenate([self.X, instruments[:, : self.num_instuments]], axis=1)
        P_H_N = np.dot(np.dot(H_N, np.linalg.inv(np.dot(H_N.T, H_N))), H_N.T)
        Y_bar_hat = np.dot(P_H_N, Y_bar)
        Z_hat = np.concatenate([self.X, Y_bar_hat], axis=1)
        delta = np.dot(np.dot(np.linalg.inv(np.dot(Z_hat.T, Z_hat)), Z_hat.T), self.y)
        return delta
