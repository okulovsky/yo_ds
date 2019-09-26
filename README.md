# `yo_ds`

This is a personal library, allowing more functional programming in Python data-science. 
Mostly, it's focused on writing code like this:

```python
from yo_extensions import *
import json

(Query
.file.text('data.jsonlines')                # read file and create a 'stream' of lines
.select(json.loads)                         # parse each line with JSON
.where(lambda z: maybe(z,'status')=='OK')   # only items with status equals OK, maybe is Elvis operator
.select(lambda z: (z['id'],z['message']))
.to_dataframe(columns=['id','message'])     # seamless integration with pandas
.groupby('message')
.size()
.feed(plots.series.pie())                   # extension method, draws a pie chart with custom settings
)
```

The key principles are:
* Fluent interface
* Type annotations
* Extendability

Contents:
* Yet another port of `C# LINQ` to Python. The closest analogue is `asq`. The key differences are: type annotation support and different extendability mechanism
* Extension methods for better data-science: plotting, status reporting, algorithms on pandas
* A few useful classes for machine-learning
* Wide test coverage for most of the implemented funcionality

## `fluq`

The port of `C# LINQ` to Python with type annotations. The usual methods (`select`, `where`) are implemented as methods of `Queryable` class.

The extension methods are challenging due to Python restrictions. I couldn't use monkey-patching, because it does not preserve type-annotations, and injected methods are not seen by IDE. Thus, the following mechanism is employed:
* Consider the function `f(q,X)` where `q` is `Queryable` and `X` is a tuple of additional argument.
* Lets _Curry_ `q`, introducing `h(X)` such that `h(X)` returns `g(q)` and so `h(X)(q)=g(q)=f(q,X)`
* To inject `h` into `q`, `q.feed` method accepts `g`, so `q.feed(h(X)) = h(X)(q) = f(q,X)`

This mechanism preserves the type annotation, allows to add any functionality to `Queryable` and almost preserves Fluent interface: you need to add `feed` instead of just chaining methods.

To avoid coding of both `g` and `h` function for any functionality, the suggested way of implementation for `h` is a class, `X` is provided in `__init__`, and also `h` is `Callable` so it can accept `q`.

The same mechanism employed for `pd.DataFrame`, `pd.Series`, `pd.DataFrameGroupBy` and `pd.SeriesGroupBy`. For these classes, `feed` is monkey-patced and does not preserve the type annotation.

## `feed`-compatible extensions

* Several extensions for `fluq`: input/output to various file types, partitioning, etc. 
* Few extensions for `pandas`: adding ordering inside groups, stratifying order for Dataframes, etc
* Plots: several plots I like to use in research, implemented in `feed`-compatible mode.

`yo_extensions/__init__.py` provides the demonstration on how better include `fluq` with extensions into the side project.

## `ml`

Small utilities:

* `kraken`: Executes _method_ with the various arguments (_plan_) and returns the result as `pd.DataFrame` for futher analysis
* `metrics`: computes lots of metrics for predicted/actual values and returns them as `pd.DataFrame`.
* `keras`: wrapper over `keras` generators.