from typing import *
from yo_fluq_ds import *
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score, roc_auc_score
import numpy as np

class MulticlassMetricType(OrderedEnum):
    General = 0
    ByClass = 1
    Global = 2

class MulticlassMetrics(Obj):
    def __init__(self,
                 metric_type: MulticlassMetricType,
                 metric_name: str,
                 metric_aggregation: Optional[str],
                 value: float):
        super(MulticlassMetrics, self).__init__()
        self.metric_type = metric_type
        self.metric_name = metric_name
        self.metric_aggregation = metric_aggregation
        self.value = value

class MulticlassByClassMetrics(Obj):
    def __init__(self, class_name: Any, metric_name: str, value: float):
        super(MulticlassByClassMetrics, self).__init__()
        self.class_name = class_name
        self.metric_name = metric_name
        self.value = value


class MulticlassMetricsComputer:
    def __init__(self,
                 global_metrics : Dict[str,Callable[[pd.Series,pd.Series],float]],
                 general_metrics: Dict[str,Callable[[pd.Series,pd.Series,str],float]],
                 general_aggregators: List[str],
                 by_class_metrics: Dict[str, Callable[[pd.Series, pd.Series], float]],
                 by_class_aggregators: Dict[str, Callable[[pd.Series], float]]
                 ):
        self.global_metrics = global_metrics
        self.by_class_metrics = by_class_metrics
        self.by_class_aggregators = by_class_aggregators
        self.general_metrics = general_metrics
        self.general_aggregators = general_aggregators

    def _get_global(self, true, predicted)->Queryable[MulticlassMetrics]:
        return (Query
                .dict(self.global_metrics)
                .select(lambda metric: MulticlassMetrics(
                    MulticlassMetricType.Global,
                    metric.key,
                    None,
                    metric.value(true,predicted)
                )))

    def _get_general(self, true, predicted) -> Queryable[MulticlassMetrics]:
        return (Query
                .en(self.general_aggregators)
                .select_many(lambda agg: Query
                             .dict(self.general_metrics)
                             .select(lambda metric: MulticlassMetrics(
                                    MulticlassMetricType.General,
                                    metric.key,
                                    agg,
                                    metric.value(true,predicted,agg)
                ))))

    def by_class_matrix(self, true, predicted) -> Queryable[MulticlassByClassMetrics]:
        classes = Query.en(true).intersect(predicted).distinct().to_list()
        return (Query
                .en(classes)
                .select_many(lambda _class: Query
                             .dict(self.by_class_metrics)
                             .select(lambda metric: MulticlassByClassMetrics(
                                    _class,
                                    metric.key,
                                    metric.value(true==_class,predicted==_class)
                ))))

    def _get_by_class(self, true, predicted) -> Queryable[MulticlassMetrics]:
        return (self.by_class_matrix(true,predicted)
                .group_by(lambda z: z.metric_name)
                .select_many(lambda group: Query
                             .dict(self.by_class_aggregators)
                             .select(lambda agg: MulticlassMetrics(
                                    MulticlassMetricType.ByClass,
                                    group.key,
                                    agg.key,
                                    agg.value([v.value for v in group])
                ))))


    def compute(self, true, predicted):
        return (self._get_general(true,predicted)
                .concat(self._get_global(true,predicted))
                .concat(self._get_by_class(true, predicted))
                )

class UniclassMetricsComputer:
    def __init__(self, metrics: Dict[str,Callable[[pd.Series,pd.Series],float]]):
        self.metrics = metrics

    def compute(self, true, predicted)->Queryable[KeyValuePair[str,float]]:
        return (Query
                .dict(self.metrics)
                .select(lambda metric: KeyValuePair(metric.key,metric.value(true,predicted)))
        )

def _wrap_general(m):
    return lambda true, predicted, agg : m(true,predicted, average = agg)

general_metrics= Obj(
    precision = _wrap_general(precision_score),
    recall = _wrap_general(recall_score),
    f1 = _wrap_general(f1_score)
)

general_aggregators = [
    'macro',
    'micro',
    'weighted'
]

by_class_metrics = Obj(
    precision = precision_score,
    recall = recall_score,
    f1 = f1_score,
    accuracy = accuracy_score
)

by_class_aggregators = Obj(
    min = lambda z: min(z),
    max = lambda z: max(z),
    mean = lambda z: np.mean(z),
    std = lambda z: np.std(z)
)

global_metrics = Obj(
    accuracy = accuracy_score
)

class Metrics:
    Uniclass = UniclassMetricsComputer(by_class_metrics)
    Multiclass = MulticlassMetricsComputer(global_metrics,general_metrics,general_aggregators,by_class_metrics,by_class_aggregators)
