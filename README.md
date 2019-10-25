## Summary

`yo_fluq` focuses on a fluent, lazy, expandable way of writing data processing pipelines. The typical example is

```python
(Query
    .en(orders)
    .take(1000)
    .where(lambda order: order['is_shipped'])
    .select(lambda order: order['payment_information'])
    .group_by(lambda payment: payment['customer_id'])
    .to_dictionary(
        lambda group: group.key,
        lambda group: Query
                        .en(group.value)
                        .select(lambda payment: payment['value'])
                        .sum()
        )
)

```

This way of writing code is typical for C# Linq and Spark, and this project makes it available for Python as well.

Unlike `pandas`, `yo_fluq` is:
* Lazy, so it does not require to keep the whole collection in memory
* Extendable, so you can define your own filters and use them in pipelines.

Unlike [`asq`](https://pypi.org/project/asq/) or [`py_linq`](https://pypi.org/project/py_linq/), well-known ports of C# LINQ to Python, `yo_fluq` fully supports data annotations, even in case of user-defined extensions. Therefore, in IDE like PyCharm you will see the available methods in the hints.
[`plinq`](https://pypi.org/project/plinq/) supports annotations, but does not offer extendability technique.

The library has been developed since 2017, is extensively tested and is currently available under MIT licence, at Beta development stage.





## Structure

This repository contains the following modules:
* `yo_fluq`
    * Does not have any dependencies on other Pypi modules
    * Python port for LINQ, or [pull-pipelines](documentation/yo_fluq_pull.md)
    * [Push-pipelines](documentation/yo_fluq_push.md)
* `yo_fluq_ds`
    * Aggregation of data into `numpy` and `pandas` data structures and files in pull- and push-queries
    * Querying `numpy`, `pandas` data structures, as well as files and combinatorics lazy sources
    * Several extension methods with no real structure, just something I use a lot
    * [Documentation](documentation/README_yo_fluq_ds.md)
* `yo_ds`
    * Experimental stuff, my own plots, etc. Highly unstable. Use at your own risk. No documentation is available.
* `yo_extensions`
    * Obsolete, used for backward compatibility. Will be removed at some point. Do not use in new projects.
