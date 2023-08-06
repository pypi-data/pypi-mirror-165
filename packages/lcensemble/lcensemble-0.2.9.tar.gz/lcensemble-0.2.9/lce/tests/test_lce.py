import numpy as np
from sklearn.datasets import load_iris, load_diabetes
from sklearn.utils.estimator_checks import check_estimator
import unittest
import warnings

from .._lce import LCEClassifier, LCERegressor


class Test(unittest.TestCase):
    """Tests of LCE"""

    def test_classifier_params(self):
        # Load Iris dataset
        data = load_iris()

        # max_depth
        with self.assertRaises(ValueError):
            LCEClassifier(max_depth=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(max_depth=1.1).fit(data.data, data.target)

        # min_samples_leaf
        with self.assertRaises(ValueError):
            LCEClassifier(min_samples_leaf=0).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(min_samples_leaf=1.1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(min_samples_leaf="a").fit(data.data, data.target)
        with warnings.catch_warnings():
            LCEClassifier(min_samples_leaf=0.3).fit(data.data, data.target)

        # n_iter
        with self.assertRaises(ValueError):
            LCEClassifier(n_iter=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(n_iter=1.1).fit(data.data, data.target)

        # verbose
        with self.assertRaises(ValueError):
            LCEClassifier(verbose=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(verbose=1.1).fit(data.data, data.target)
        with warnings.catch_warnings():
            LCEClassifier(verbose=1).fit(data.data, data.target)

    def test_classifier_missing(self):
        # Load Iris dataset
        data = load_iris()

        # Input 2% of missing values per variable
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCEClassifier(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

        # Input 20% of missing values per variable
        np.random.seed(0)
        m = 0.2
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCEClassifier(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

        # Input 60% of missing values per variable
        np.random.seed(0)
        m = 0.6
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCEClassifier(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

        # Input 100% of missing values per variable
        np.random.seed(0)
        m = 1.0
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCEClassifier(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

    def test_classifier_sklearn_estimator(self):
        # scikit-learn check estimator
        assert check_estimator(LCEClassifier()) == None

    def test_regressor_params(self):
        # Load Diabetes dataset
        data = load_diabetes()

        # max_depth
        with self.assertRaises(ValueError):
            LCERegressor(max_depth=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(max_depth=1.1).fit(data.data, data.target)

        # min_samples_leaf
        with self.assertRaises(ValueError):
            LCERegressor(min_samples_leaf=0).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(min_samples_leaf=1.1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(min_samples_leaf="a").fit(data.data, data.target)
        with warnings.catch_warnings():
            LCERegressor(min_samples_leaf=0.3).fit(data.data, data.target)

        # n_iter
        with self.assertRaises(ValueError):
            LCERegressor(n_iter=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(n_iter=1.1).fit(data.data, data.target)

        # verbose
        with self.assertRaises(ValueError):
            LCERegressor(verbose=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(verbose=1.1).fit(data.data, data.target)
        with warnings.catch_warnings():
            LCERegressor(verbose=1).fit(data.data, data.target)

    def test_regressor_missing(self):
        # Load Diabetes dataset
        data = load_diabetes()

        # Input 2% of missing values per variable
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            LCERegressor(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                temp, data.target
            )

        # Input 20% of missing values per variable
        np.random.seed(0)
        m = 0.2
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCERegressor(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

        # Input 60% of missing values per variable
        np.random.seed(0)
        m = 0.6
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCERegressor(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

        # Input 100% of missing values per variable
        np.random.seed(0)
        m = 1.0
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            data.data[sub, j] = np.nan

        with warnings.catch_warnings():
            LCERegressor(max_depth=50, min_samples_leaf=1, random_state=0).fit(
                data.data, data.target
            )

    def test_regressor_sklearn_estimator(self):
        # scikit-learn check estimator
        assert check_estimator(LCERegressor()) == None
