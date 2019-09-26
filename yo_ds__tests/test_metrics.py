import unittest
from yo_ds__tests.common import *
import pandas as pd
from yo_ds.metrics import Metrics, roc_optimal_threshold

uniclass = pd.DataFrame(dict(
    true = [0,0,0,0,0,1,1,1,1,1],
    predicted = [0,0,0,1,1,1,1,0,0,0]
))

multiclass = pd.DataFrame(dict(
    true = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    predicted = [0, 0, 1, 2,  1, 2, 0, 0, 0, 1, 0, 2, 2, 2]
))

roc = pd.DataFrame(dict(
    true = [0, 0, 0, 0, 1, 1, 1],
    predicted = [0.1, 0.2, 0.3, 0.6, 0.5, 0.8, 0.9]
))

class MetricsTests(unittest.TestCase):
    def test_uniclass(self):
        series = Metrics.Uniclass.compute(uniclass.true, uniclass.predicted).to_series()

    def test_multiclass_matrix(self):
        matrix = Metrics.Multiclass.by_class_matrix(multiclass.true,multiclass.predicted).to_dataframe().sort_values('metric_name')

    def test_multiclass(self):
        metrics = Metrics.Multiclass.compute(multiclass.true, multiclass.predicted).to_dataframe().drop('metric_type',axis=1)

    def test_roc_auc(self):
        threshold = roc_optimal_threshold(roc.true,roc.predicted)
        self.assertEqual(0.5,threshold)