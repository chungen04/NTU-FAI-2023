import numpy as np


"""
Implementation of Principal Component Analysis.
"""
class PCA:
    def __init__(self, n_components: int) -> None:
        self.n_components = n_components
        self.mean = None
        self.components = None

    def fit(self, X: np.ndarray) -> None:
        #TODO: 10%
        mean = np.mean(X, axis=0)

        # Subtract the mean from each column
        X_norm = X - mean
        XTX = X_norm.transpose().dot(X_norm)
        # print(XTX.shape)
        eigenvec = np.linalg.eig(XTX)
        print(eigenvec)
        raise NotImplementedError

    def transform(self, X: np.ndarray) -> np.ndarray:
        #TODO: 2%
        raise NotImplementedError

    def reconstruct(self, X):
        raise NotImplementedError
        #TODO: 2%
