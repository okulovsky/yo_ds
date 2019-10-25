# `yo_fluq`

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





## Pull-pipelines

`yo_fluq` is a port of [C# LINQ-to-objects](https://en.wikipedia.org/wiki/Language_Integrated_Query#LINQ_to_Objects), which is a set of methods for data processing, focused on:
* [Fluent interface](https://en.wikipedia.org/wiki/Fluent%20interface)
* [Lazy evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation)
* Extendability
* Type hints

This port maintains this focus. 

### Motivation

Consider the task:
* You have two collections of `articles` and `customers`
* You have a `function` that predicts how well the article fits the customer
* You want to get the top-10 tuples of `(article, customer, value)`, but only if the function’s value is greater than 0
* These tuples have to be sorted by `value` in descending order

#### Naive Python

The easiest way to solve it is to just write it in Python:

```python
result = []
for article in articles:
    for customer in customers:
        value = function(article,customer)
        if value>0:
            result.append((article,customer,value))
result.sort(key = lambda z: z[2], reverse = True)
return result[:10]
```
The problems are:
* The code gets more and more nested with every step, which contributes to poor code quality
* Everything is done in a different way: we use operators for filtering, function with and without returning values for different cases. It's not uniform
* If you want to restore the task from this code, it requires an effort. The code is not self-explanatory

#### List comprehension

List comprehension is another way of doing it:
```python
result = [
    (article,customer,function(article,customer))
    for article in articles
    for customer in customers
    if function(article,customer) > 0
]
result.sort(key = lambda z: z[2], reverse = True)
return result[:10]
```

The problems are:
* The functionality is limited and non-extendable. In order to put filtration inside list comprehension, I had to compute `function` twice. Ordering and slicing are impossible to fit
* I use `article` and `customer` before they are defined. Hence, no type hints will be available in IDE
* (subjective) The syntax is rather exotic

#### `pandas`

If we convert the whole data in pandas, it's easy to do:

```python
df = pd.DataFrame(
    [(article, customer) for article in articles for customer in customers],
    columns = ['article','customer'])
df = (df
    .assign(value = df.apply(lambda s: function(s.article,s.customer),axis=1))
)
return (df
    .loc[df.value>0]
    .sort_values('value',ascending=False)
    .iloc[:10]
)
```

Here we have **Fluent** Interface, and it brings:
* We can apply more and more filters, just adding the lines
* Everything is done in the same **uniform** fashion: all the filters are just methods of `pandas`
* Code is readable: each line of code basically can be traced to the line in problem's description

However, there are still problems:
* It's not always easy to convert data from existing format to pandas, you need to write some (ugly) code for that
* In some cases it's not possible. Pandas requires the whole dataframe to be in memory, which is sometimes not possible
* Not all the data are two-dimensional
* `pandas` is still not extendable: I had to break a fluent style once to filter out by `value`. 

#### `itertools`

The survey of different methods won't be complete without the fourth method - `itertools`:

```python
return islice(
    sorted(
        filter(
            lambda z: z[2]>0,
            map(
                lambda art_cust: (
                    art_cust[0], 
                    art_cust[1], 
                    function(art_cust[0],art_cust[1])),
                product(
                    articles,
                    customers
                )                
            )
        ),
        key = lambda res: res[2],
        reverse=True
    ),
    0,
    10
)
```   

This method solves all the problems of pandas:
* By default, all the itertools are **lazy**: that means, you don't need to store all the data in memory at once
* It's extendable: you can always write your own method to do precisely what you need. This whole code is written completely within one approach
* Applicable to any data in any format

However:
* `itertools` has horrible inside-out syntax which is almost unreadable.

#### `fluq`

This is the solution, offered by this module:

```python
(Query
    .combinatorics.cartesian(articles,customers)
    .select(lambda art_cust: art_cust+(function(art_cust[0],art_cust[1]),))
    .where(lambda res: res[2]>0)
    .order_by_descending(lambda res: res[2])
    .take(10)
    .to_list()
)
```

This solution is combining the best parts of `pandas` and `itertools`. It is fluent, lazy, 
* Fluent
* Lazy
* Extendable: you can add your own filter
* After each dot `.` in IDE you can see the list of methods applicable, so half of this query will be written by IDE.

### Related works

Of course, I didn't invent this solution. I learned it from `C#`, which employed ideas from `Scala` (the same concepts are behind Spark for instance). 

What I did is port to Python. 

I know about these analogues:

* [`asq`](https://github.com/sixty-north/asq), [`py-linq`](https://pypi.org/project/py_linq/). The key difference is that `yo_fluq` has annotations and it's expansion technique preserves type hints
* [`plinq`](https://pypi.org/project/plinq/) has type annotations, but does not have an extendability mechanism.
* [`RxPy`](https://github.com/ReactiveX/RxPY) contains LINQ port, which is non-extendable and is not a main focus of the library anyway.
* In some sense [`fluentpy`](https://github.com/dwt/fluent). However the approach of this module is more fundamental, and that leads to the side effects described in the repo.


### Fluent data processing

The typical `fluq` pipeline looks like this:

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

The typical `fluq` pipeline consists of:
* The source `Query.en(orders)`. This creates the `Queryable` object which can be perceived as a flow of objects
* The set of filters `where`, `select`, `take`, `group_by`
* The final aggreagation `to_dictionary`, that initiates all other components and produces the result.

#### Sources

| Code | Arguments | Output type | Comments |
| ---- | --------- | ----------- | -------- |
| `Query.en(list)`        | `list: Iterable[T]`     | `Q[T]` |
| `Query.args(*args)`     | `*args: Any`            | `Q[Any]` | Mostly used in unit tests
| `Query.dict(dict)`      | `dict: Dict[TKey,TValue]` | `Q[KeyValuePair[TKey,TValue]]` | Use Query.en(dict.values()) or Query.en(dict) to access only keys or values
| `Query.loop(begin,delta,end,endtype)` | | `Q[Any]` | Produces begin, begin+delta, begin+delta+delta, etc. until the end. Also works when delta is negative. `endType` determines when exactly process ends.

Notes:
* `Query` is a singleton instance of `QueryFactory` class that contains all the sources.  
* `Q` is used as a shortening for `Queryable` through all this documentation
* The annotations in code may be weaker than in documentation. Currently, annotations are messy in the library, basically I only worried that type hints work in PyCharm 

#### Filters

##### Main filters

For these filters it is important to understand what is the type of the incoming and outgoing objects. 

| Method | Input | Argument | Output | Comments |
| ------ | ----- | -------- | ------ | -------- |
| `select(selector)`        | `Q[TIn]`        | `selector:` `TIn->TOut`           | `Q[TOut]`             | Maps elements of the flow. Preserves length. Analog to itertools.map
| `where(filter)`           | `Q[T]`          | `filter:` `T->bool`               | `Q[T]`                | Stops the elements where filter's value is False. Analog to itertools.filter
| `distinct(selector)`      | `Q[T]`          | Opt. `selector:` `T->Any`          | `Q[T]`                | Distinct elements. By some value if `selector` is provided
| `select_many(selector)`   | `Q[TIn]`        | `selector:` `TIn->Iterable[TOut]`   | `Q[TOut]`             | Like `select`, but flattens the result, so returns `Q[TOut]` instead of e.g. `Q[List[TOut]]`.
| `with_indices()`          | `Q[T]`          |                                 | `Q[KeyValuePair[int,T]]` | Enumerates objects in the incoming flow
| `group_by(selector)`       | `Q[T]`          | `selector:` `T->TKey`              | `Q[KeyValuePair[TKey,List[T]]` | Groups elements by the key, provided by selector, and propagates the groups. 

##### Flow control and set operations

Flow control and set operations:
* `skip(N)` skips N objects in the flow
* `take(N)` takes N objects from the flow, then stops processing. 
* `skip_while(condition)` skips objects while condition is true, then start processing them ignoring the condition
* `take_while(condition)` process objects while condition is true, then stops processing
* `prepend(*args)` places `*args` in front of the flow
* `append(*args)` places `*args` after the flow
* `Query.en(e1).concat(e2)` concatenates collections e1 and e2 in the flow
* `Query.en(e1).intersect(e2)` intersects the collection e1 and e2

##### Ordering

* `order_by(key_selector)` and `order_by_descending(key_selector)` will order the flow by ascending/descending values of the `key_selector`
* If ordering by several keys is needed, add them with `then_by`/`then_by_descending`.

Example:

```python
(Query
    .en(['B1','A0','A1','B1'])
    .order_by(lambda element: element[0])
    .then_by_descending(lambda element: element[1])
    .to_list()
    )
``` 
will order the collection by the ascending first letter, and then by the descending second letter, producing `['A1','A0','B1','B0']`


#### Aggregators

Each aggregator exists in two forms: as a method in Queryable, and as a class in `agg` module. The reason is, that aggregators are reused in both pull- and push-queries. The names are self-explanatory:
* Getters: `first`, `last` and `single` (works like `first` but throws exception if more than element occur)
* Basic math: `sum`, `count`, `mean`, `std`, `max`, `min`
* `arg_max` and `arg_min` (accepts `selector`, return the element for which its value is highest/lowest)
* `all`, `any`

#### Others

The following methods are also implemented:
* `foreach(processor)` acts as aggregator, executes `processor` on each element in the flow
* `foreach_and_continue(processor)` execute processor on each element in the flow, but let flow further, thus acting like a filter
*  `parallel_select` runs `select` in parallel, thus simplifying multiprocessing usage in Python, if you want to speed-up some really time-consuming `select`.

### Execution order

Consider the query

```python
(Query
    .en([0,1,2])
    .where(lambda z: z%2==0)
    .select(str)
    .to_list()
)    
```

_You might think_ that it first filters out the odd numbers, then translates what is left into strings, and then puts the numbers to list. 
The actual process you might see in the debugger is different, but lead to the same result.

| Enumerable | Query | Effective python code|
| --- | --- | --- | 
| en1 | `Query.en([0,1,2])` |`for z0 in [0,1,2]: yield e` |
| en2 | `e1.where(lambda z: z%2==0)` | `for z1 in en1: if z1%2==0: yield z1` | 
| en3 | `e2.select(str)`  |  `for z2 in en2: yield str(e2)` | 
|     | `e3.to_list()`    | `for z3 in en3: lst.append(z3)` | 

The sequence of actions is:
* `to_list` requests element from `en3`
    * `en3` is the result of `select`, so `select` requests element from `en2`
    * `en2` is the result of `where`, so `where` requests element from `en1`
    * `en1` iterates over `[0,1,2]`. First `z0` is `0`, this is yielded as `en1` element
    * `where` checks `z1=0`, it satisfies the condition, `where` yields `0`
    * `select` converts `0` to `'0'` and yields it
    * `to_list` places `z3='0'` into `lst`
* `to_list` requests next element from `en3`
    * `select` requests next element from `en2`
    * `where` requests next element from `en1`
    * `1` is the next element in `[0,1,2]`. So it is yielded
    * `where` checks this element, it does not satisfy the condition
    * `where` requests another element from `en1`
    * `2` is the next element in `[0,1,2]`, so `2` is yielded as the next element in `en1`
    * `where` checks `2`, it satisfies the condition and is yielded as `en2` _second_ element
    * `select` converts `2` to `'2'`
    * `to_list` places `'2'` into `lst`
* `to_list` requests next element from `en2`
    * `select` requests next element from `en2` 
    * `where` requests next element from `en1`
    * There is no more elements in `[]`, so loop in `en1` terminates
    * `where`'s loop terminates
    * `select`'s loop terminates
    * `to_list`'s loop terminates 
    


### Extendability

In C#, there are [extension methods](https://en.wikipedia.org/wiki/Extension_method), the syntax which "add" a method to compiled object. 
In Python, monkey-patching produces the similar effect, but unfortunately neither PyCharm nor Jupyter Notebook can infer the annotations for monkey-patched methods.
Therefore, extendability and type hints come into conflict in Python, and this section describes how the conflict is resolved.   

#### `feed`-method

`feed` method in `Queryable` is defined as:

```python
def feed(self, processor: Callable[[Queryable],T]) -> T:
    return processor(self)
``` 

Assume we want to extend with [TQDM](https://pypi.org/project/tqdm) progress bar:

```python
def _with_tqdm_iter(queryable):
    for element in tqdm(queryable):
        yield element
        
def with_tqdm(queryable: Queryable) -> Queryable:
    return Queryable(_with_tqdm_iter(queryable))
```

Now, the code:

```python
Query.en([1,2,3]).feed(with_tqdm).to_list()

```
will push the flow through the tqdm and produce a list [1,2,3]. Due to type annotation for `feed` and `with_tqdm` methods, the type of the expression `Query.en([1,2,3]).feed(with_tqdm)` can be inferred as `Queryable`, thus the type hint will appear.

What if you want to pass some arguments to this `with_tqdm` method? Then it's a little more complicated:

```python
class with_tqdm(Callable[[Queryable],Queryable]):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def _with_tqdm_iter(self, queryable):
        for element in tqdm(queryable, **self.kwargs):
            yield element
            
    def __call__(self, queryable: Queryable) -> Queryable:
        return Queryable(self._with_tqdm_iter(queryable))
```

And then:

```python
Query.en([1,2,3]).feed(with_tqdm(total=3)).to_list()
```

So if you want to develop several extension methods, just follow these templates and you will keep the type hints. 

#### Updating Query and Queryable

At some point, there are simply too much of the extension methods used too often, so the pipeline looks like a sequence of `feed` methods.

In order to resolve that, there is a need to re-define `Queryable`, so:
* the old `Queryable` methods produce instances of new `Queryable`
* the annotation is bound to the new `Queryable` in both old and new cases.

Fortunately, this is possible, and done in the `yo_fluq_ds` package. I refer you to the source code for details, because this is definitely not the most frequently needed operation. 

## Push-queries

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

### Push-queries architecture

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


### Expandability

Since push-queries are just sequences of factories, you can always write your own PQE and add it to the sequence with `append` method of `PushQuery`. No special magic is required.

The base class for PQE is `PushQueryElement`. As instances, it creates `_PushQueryElementInstance` objects, but these objects redirect all their methods to the factory. It is very important to **never** modify anything that belongs to the factory in these methods, otherwise it's hard to predict the system's behavior.

### Comparing pull- and push-queries

New filters for pull-queries are very easy to write with `yield`. However, push-queries are harder to write: in complex cases, when the processing of element is affected by processing the previous, you must write state machine yourself, while in pull-queries it is done by Python.

Pull-queries can be easily continued with push-queries, and actually this happens always, because aggregators in pull-query are implemented as atomic push-queries. However, push-query can be continued with pull-query only in a separate thread. There is no other means to do that.

In general, for data processing, the pull-queries are the weapon of choice. Push-queries should only be used for the cases, when the data flow "splits" and forms trees, like in `group_by`-based statistics.

