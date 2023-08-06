import numpy as np
from typing import List
from scipy.optimize import minimize


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
        self.params = None

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
        self._delta = self._TSLS()
        self._resid = (
            self.y
            - np.dot(self.X, self._delta[: self.X.shape[1]])
            - sum(
                [
                    self._delta[self.X.shape[1] + i] * np.dot(weight_matrix, self.y)
                    for i, weight_matrix in enumerate(self.W)
                ]
            )
        )
        self._rho = self._GMM()
        self.params = np.concatenate([self._delta, self._rho])

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

    def get_params(self) -> np.ndarray:
        """Return estimated model parameters

        :return: Estimated model parameters. [beta, delta, rho]
        :rtype: np.ndarray
        """
        assert self.params is not None, "Fit model first"
        return self.params

    def _GMM(self) -> np.ndarray:
        """Perform a GMM estimation step for autoregressive disturbances

        :return: Rho parameter estimates
        :rtype: np.ndarray
        """
        S = len(self.M)
        x_0 = np.array([0.01 for _ in range(int(2 * S + S * (S - 1) / 2))])
        rho = minimize(self._objective_function, x_0, method="Nelder-Mead")
        return rho.x[:S]

    def _objective_function(self, b: np.ndarray) -> np.ndarray:
        """Calculate moment conditions and then the value of the GMM objective function under a set of parameter values.

        :param b: input parameters
        :type b: np.ndarray
        :return: objective function value
        :rtype: np.ndarray
        """
        u_bar = np.array(
            [np.dot(resid_weight_matrix, self._resid) for resid_weight_matrix in self.M]
        )
        u_bar_bar = np.array(
            [
                [np.dot(resid_weight_matrix, u) for u in u_bar]
                for resid_weight_matrix in self.M
            ]
        )
        A_1 = [
            [
                np.dot(s_prime.T, s)
                - np.diag(
                    np.array(
                        [np.dot(s_prime[:, i].T, s[:, i]) for i in range(s.shape[0])]
                    )
                )
                for s in self.M
            ]
            for s_prime in self.M
        ]
        A_2 = self.M
        S = len(self.M)
        gamma_tilde = [None for _ in range(int(2 * S + S * (S - 1) / 2))]
        Gamma_tilde = np.array(
            [
                [None for _ in range(int(2 * S + S * (S - 1) / 2))]
                for _ in range(int(2 * S + S * (S - 1) / 2))
            ]
        )
        for s in range(S):
            for s_prime in range(S):
                if s > s_prime:
                    continue
                if s == s_prime:
                    rownum = 2 * s + 1
                else:
                    rownum = 2 * S + s * S - s * (s + 1) / 2 + s_prime - s
                index = int(rownum - 1)
                gamma_tilde[index] = (
                    1
                    / self.N
                    * np.dot(np.dot(self._resid.T, A_1[s][s_prime]), self._resid)
                )
                for i, resid_weight_matrix in enumerate(self.M):
                    Gamma_tilde[index, i] = (
                        2
                        / self.N
                        * np.dot(
                            np.dot(
                                np.dot(self._resid.T, resid_weight_matrix.T),
                                A_1[s][s_prime],
                            ),
                            self._resid,
                        )
                    )
                    Gamma_tilde[index, i + S] = (
                        -1
                        / self.N
                        * np.dot(
                            np.dot(
                                np.dot(
                                    np.dot(self._resid.T, resid_weight_matrix.T),
                                    A_1[s][s_prime],
                                ),
                                resid_weight_matrix,
                            ),
                            self._resid,
                        )
                    )
                for ss in range(S):
                    for ss_prime in range(S):
                        if ss_prime > ss:
                            m = ss + 1
                            l = ss_prime + 1
                            Gamma_tilde[
                                index, int(S * (m + 1) - m * (m - 1) / 2 + l - m - 1)
                            ] = (
                                -2
                                / self.N
                                * np.dot(
                                    np.dot(
                                        np.dot(
                                            np.dot(self._resid.T, self.M[s_prime].T),
                                            A_1[s][s_prime],
                                        ),
                                        self.M[s],
                                    ),
                                    self._resid,
                                )
                            )
            gamma_tilde[2 * s + 1] = (
                1 / self.N * np.dot(np.dot(self._resid.T, A_2[s]), self._resid)
            )
            for i, resid_weight_matrix in enumerate(self.M):
                Gamma_tilde[2 * s + 1, i] = (
                    1
                    / self.N
                    * np.dot(
                        np.dot(
                            np.dot(self._resid.T, resid_weight_matrix.T),
                            A_2[i] + A_2[s],
                        ),
                        self._resid,
                    )
                )
                Gamma_tilde[2 * s + 1, S + i] = (
                    -1
                    / self.N
                    * np.dot(
                        np.dot(
                            np.dot(
                                np.dot(self._resid.T, resid_weight_matrix.T), A_2[s]
                            ),
                            resid_weight_matrix,
                        ),
                        self._resid,
                    )
                )
            for ss in range(S):
                for ss_prime in range(S):
                    if ss_prime > ss:
                        m = ss + 1
                        l = ss_prime + 1
                        Gamma_tilde[
                            2 * s + 1, int(S * (m + 1) - m * (m - 1) / 2 + l - m - 1)
                        ] = (
                            -1
                            / self.N
                            * np.dot(
                                np.dot(
                                    np.dot(
                                        np.dot(self._resid.T, self.M[s_prime].T),
                                        (A_2[ss] + A_2[ss_prime]),
                                    ),
                                    self.M[s],
                                ),
                                self._resid,
                            )
                        )

        v = gamma_tilde - np.dot(Gamma_tilde, b)
        return np.dot(v.T, v)
