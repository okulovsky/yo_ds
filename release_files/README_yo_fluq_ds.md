# `yo_fluq_ds`

This package is an data science-specific update for [`yo_fluq`](https://pypi.org/project/yo-fluq/) that introduces:
* querying and output for `pandas` data structures and files in `Queryable`
* handy `feed`-based extension methods.

The main reason for separating `yo_fluq_ds` from `yo_fluq` is that data science functionality requires huge packages like `pandas` and `matplotlib`, which I didn't want to include in a basic package.

## Small useful classes

* `Obj` is an ordered dict with a member-like access: `obj.a=12` works exactly as `obj['a']=12`
* `OrderedEnum` is `Enum` with ordering, it's useful when using enums in `pandas`, because the basic enumeration cannot be used as keys for `group_by`

## Pull-queries updates

### Combinatorics

`Query.combinatorics` has some useful method to create lazy combinatorics enumerations:
* `cartesian(en1,en2,...)` will create a cartesian product of enumerations in `en1`, `en2`, etc.
* `grid(field1=en1,field2=en2)` will create an enumeration of `Obj` with fields `field1`, `field2` that runs over cartesian product of `en1`, `en2`, etc.
* `triangle` is query-like replacement for loops `i=0..N`, `j=0..i`
* `powerset` produces all the subsets of a given set

### File system

Adds several aggregators/query sources to work with files.

* `to_text_file`/`Query.file.text`: text file, its lines are interpreted as enumeration's objects
* `to_zip_file`/`Query.file.zipped_text`: zipped text file
* `to_pickle_file`/`Query.file.pickle`: a internal format, lazily writes a sequence of objects in pickle format in one file.
* `to_zip_folder`/`Query.to_zipped_folder`: representation for `KeyValuePair`: filenames are keys, its concent is values

Adds `FileIO` class with one-line instruction to read text, json, pickle, jsonpickle, yaml files.

Adds `Query.folder` method to create enumeration of `Path` objects from folder

### `pandas`

* Adds `to_series`, `to_dataframe` and `to_ndarray` aggregators
* Adds `Query.series` to convert series in `KeyValuePair` enumeration
* Adds `Query.df` to convert dataframe in `Obj` (or `dict`) enumeration

Adds `feed` method to `DataFrame`, `Series`, `DataFrameGroupBy` and `SeriesGroupBy` by monkey-patching. It is now possible to write something like:
```python
(df
    .loc[df.status=='shipped']
    .feed(lambda z: groupby(z.date.dt.to_period('M')))
    .size()
)
```
When calling lambda inside `feed`, `z` will be assigned to the dataframe after filtering out.

This technique allows longer fluent instructions for `pandas`, which is otherwise impossible due to filtering.

## `feed`-extension methods.

Some methods from `yo_fluq_ds` are not incorporated into `Queryables`, because they are used not that often and I want to avoid overloading `Queryable` with such methods. So, they are accessible only via `feed` method.

All of them are inside `fluq` module.

### For `Queryable`

* `fluq.with_progress_bar` is a Queryable-friendly wrapping over `tqdm`. It automatically detects notebooks/console environments. The `total` (length of enumerable) in most cases is known from `Queryable.length` field, but sometimes needs to be provided.
* `fluq.with_plots(columns,figsize)` will create plots for each of elements in enumerable and return the enumerable of `ItemWithAx`. Very handy to draw several plots at once, e.g. for different columns in dataframe
* `fluq.pairwise` converts enumerable to the enumerable of pair of neighbouring elements

### For `pandas`

* `fluq.fractions` can be used where size is normally used to determine the relative size of the groups
* `fluq.trimmer` can be used to trim too high/too low values from the series, thus facilitating histograms' creation.




