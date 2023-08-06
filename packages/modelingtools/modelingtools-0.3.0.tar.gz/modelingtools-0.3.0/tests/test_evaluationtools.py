from ctypes import ArgumentError
import unittest
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from modelingtools import evaluationtools as et

class TestEvaluationTools(unittest.TestCase):

    def setUp(self):
        self.y_true= np.array([1,0,1,0,1])
        self.y_pred_train = np.array([1,1,1,0,1])
        self.y_pred_test = np.array([1,0,0,1,1])

    def mse(self, y, y_hat):
        return np.mean((y - y_hat)**2)

    def test_error_decomposition(self):
        error_df = et.error_decomposition(
            self.y_true, 
            self.y_pred_train, 
            self.y_pred_test,
            roc_auc_score, 
            0.01)
        vals = error_df.values
        self.assertEqual(vals[0:].all(), np.array([0.01, 0.00]).all())
        self.assertIsInstance(error_df, pd.DataFrame)

    def test_error_decomposition_raises_error(self):
        with self.assertRaises(ArgumentError): 
            et.error_decomposition(
                self.y_true, 
                self.y_pred_train, 
                self.y_pred_test, 
                "something", 
                0.01)


if __name__ == '__main__':
    unittest.main()
