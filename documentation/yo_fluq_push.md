# Push-queries

Push-queries are important for data aggregation. Assume you want to execute this pull-query:

```python
(Query
    .en(orders_from_huge_file())
    .where(lambda order: order['is_shipped'])
    .group_by(lambda order: order['shipping_country'])
    .to_dictionary(
        lambda group: group.key,
        lambda group: Query.en(group.value).select(lambda order: order['billing_total']).mean()
    )
)
```

The execution of the pull-query starts from the end. `to_dictionary` aggregation requests data from the filters before. 
The previous filter is `group_by`, and it can only provide data when all the file is read. Therefore, this whole file will be stored in memory, which is not possible if the file is huge. 
Therefore, this particular operation cannot really be performed by pull-queries.

Push-queries are introduced to solve this problem.

```python
pipeline = (Query
                .push()
                .where(lambda order: order['is_shipped'])
                .split_by_groups(lambda order: order['shipping_country'])
                .mean()
            )
report = pipeline(orders_from_huge_file())
```

The idea behind the this implementation is pretty much alike  [`RxPy`](https://github.com/ReactiveX/RxPY). The differences are:
* It is optimized for data processing, so pipeline has "two ways": data comes in and in the end the report comes out.
* It has the same interface as pull-queries and reuse some of their code

## Push-queries architecture

* `PushQuery` is a class that follows [Builder pattern](https://en.wikipedia.org/wiki/Builder_pattern). It's methods, like `where` or `select`, creates instances of `PushQueryElement`-s and stores them inside the class. Thus, `PushQuery` is a sequence of `PushQueryElement`, or `PQE`.
* `PushQueryElement` *is not* the entity that processes data. It is the factory that creates such entities: `PushQueryElementInstance`, or `PQEI`.
* PQEI implements `__enter__` and `__exit__` function. It must be entered to before processing data, and exited from after processing. E.g., PQEI that writes to files will close the file on exit.

So when we try to feed data to `PushQuery`, we actually:
1. Take the first PQE-factory in the `PushQuery` list.
1. Create PQEI with this factory and enter to it
1. Feed data to first PQEI. If there are more than one PQE in query, subsequent PQEI will be created and data will be forwarded to them.
1. After data is over, collect the report from PQEI. If there is more that one PQE in the query, PQEI requests report from subsequent PQEI and may transform it.
1. Exit the PQEI

Depending on its type and purpose, PQEI processes data in following fashions:
* PQEI for `sum`, `mean` etc. compute reports. If `PushQuery` consists of only one such `PQE`, it's behavior is straightforward: process data and return a report.
* PQEI for `select` transforms data and feeds it to the subsequent PQEI
* PQEI for `where` checks the condition and depending on the result, forwards it to the subsequent PQEI or discards.
* PQEI for `group_by` checks the group key and:
    * If this key is seen for the first time, creates a new instance of subsequet PQEI and forwards data to it, keeping a link to this PQEI
    * If the key was seen before, forwards data to the kept PQEI
    * Thus, `group_by` expands the original pipeline of PQE into *tree* of PQEI.

`sum`, `mean` and others are actually the very same `agg.Sum`, `agg.Mean` etc. that are used in the pull-queries.


## Expandability

Since push-queries are just sequences of factories, you can always write your own PQE and add it to the sequence with `append` method of `PushQuery`. No special magic is required.

The base class for PQE is `PushQueryElement`. As instances, it creates `_PushQueryElementInstance` objects, but these objects redirect all their methods to the factory. It is very important to **never** modify anything that belongs to the factory in these methods, otherwise it's hard to predict the system's behavior.

## Comparing pull- and push-queries

New filters for pull-queries are very easy to write with `yield`. However, push-queries are harder to write: in complex cases, when the processing of element is affected by processing the previous, you must write state machine yourself, while in pull-queries it is done by Python.

Pull-queries can be easily continued with push-queries, and actually this happens always, because aggregators in pull-query are implemented as atomic push-queries. However, push-query can be continued with pull-query only in a separate thread. There is no other means to do that.

In general, for data processing, the pull-queries are the weapon of choice. Push-queries should only be used for the cases, when the data flow "splits" and forms trees, like in `group_by`-based statistics.

