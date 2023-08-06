# aigov_libs

A library for tracking and summarizing data lineages.

## License

This library is delivered under the [International License Agreement for Non-Warranted Programs](https://www14.software.ibm.com/cgi-bin/weblap/lap.pl?li_formnum=L-DHMI-CEQ82R).

## Description

This module provides APIs to track and summarize data lineages where the data lineage
is a chain of method calls that are required to compute particular column or table data
(e.g., Series objects, DataFrame objects).
The current version of the tracking module covers almost all the pandas APIs and
some numpy APIs (e.g., binary operators). The typical process to display the data lineages
are as follows.
1. create a Tracking object to start tracking the calls by `tracking.start()`.
2. obtain the analysis targets for summarizing the data lineages.
   In case of collecting the data lineages relevant to a DataFrame object taken
   by `fit` methods, you can use `Tracking.get_fit_targets()`.
3. analyze and summarize the calls using `Tracking.make_triples()`.
4. format the summaries of the calls using `Tracking.format_summary()`.


### Limitations

* The analysis of the data lineages is performed mainly focusing on column names.
  It doesn't distinguish two columns (two Series objects) that have the same name.
* The tracking module is not designed to be performed with a multi-threaded program.
* If an uncovered API is called to compute data, only the consecutive calls of covered
  APIs are obtained as the data lineage.



## APIs:

### Functions of the aigov_libs.tracking module

#### start()
creates an instance of the Tracking class and starts tracking execution logs.

##### Returns
* tr: Tracking

##### Examples
```
from aigov_libs import tracking
tr = trackng.start()
...
```
```
from aigov_libs import tracking
with tracking.start() as tr:
  ...
```

#### end(tr)
removes the execution logs

##### Parameters
* tr: Tracking
 

### Methods of the Tracking class

#### get_fit_targets(self, params=None, estimator=None, module_name=None)
returns internal representations representing the values taken by `fit()`.

##### Parameters
* params: array-like (optional)
  - If you specify parameter names of `fit()` (e.g., params=['X']),
  only the internal representations of the values taken by the
  corresponding parameters of `fit()` are turned.
* estimator: class or str (optional)
  - If you specify an estimator, this method addresses only the `fit()`
  method of the specified estimator.
* module_name: str (optional)
  - If you specify a module name, this method addresses only the `fit()`
  methods defined in the specified module.

##### Returns
* objs: set[str]  
  - internal representations representing the values taken by `fit()`

##### Examples
```
tr.get_fit_targets(estimator=LinearRegression)   # use the class object
      tr.get_fit_targets(estimator='LinearRegression') # use the estimator name
      tr.get_fit_targets(module_name='sklearn')        # use the module name
```


#### encode_object(self, objs)
converts given objects into internal representations that can be understood by `make_triples()`.

##### Parameters
* objs: list[Any]

##### Returns
* objs: set[str]
  - a set of internal representations.
  Note that there may be more than one representation corresponding to each object.


#### make_triples(self, targets, ignore_set=True, ignore_get=True, reorder=True)
ceates a dependency graph while making summaries. The summary is in the form of
{'key': [(output,expr), ...], ...} where `expr` is either `str` or `tuple` of `expr`.

##### Parameters
* targets: list[str]
  - `make_triples` collects executed statements that are required for computing values
  represented by `targets`.
* ignore_set: bool (default=True)
  - If `ignore_set = True`, every calls of `DataFrame.__setitem__` is excluded
  from the statements of the summaries.
* ignore_get: bool (default=True)
  - If `ignore_get = True`, every calls of `DataFrame.__getitem__` is excluded
  from the statements of the summaries.
* reorder: bool (default=True)
  - If `reorder = True`, all the list of statements in the summaries are sorted
  in the execution order.

##### Returns
* triples: set[tuple]
  - each tuple represents (sources, relation, destinations).
* summaries: dict[str:dict[...]]
  - There are three types of summary: summaries['def'], summaries['use'], summaries['tbldef'].
  Each summary is in the form of {'key': [(output,expr), ...], ...}.


#### format_summary(summary, simple=False, single_line=False, ellipsis=None, repr_stmt=None, reducer=None, yield_symbol=None)
converts a given summary into a human-readable and JSON-serializable format.

##### Parameters:
* simple: bool (default=False)
  - This flag is used to determine if a resulting summary is generated in a simpler format or not.
* single_line: bool (default=False)
  - This flag is used to determine if statements in a resulting summary are formatted in a single line or not. If `single_line = True`, the statements are joined Otherwise, the statements are represented by a list of the statements where each of the statements is formatted by `repr_stmt`.
* ellipsis: str (default=None)
  - If `ellipsis` is given, every object except table-like or column-like object is replaced with the value of `ellipsis`.
* repr_stmt: (str,str,str)->Any (default=None)
  - This function is effective only when `single_line = False` and used to format executed statements which are represented in the form of `(output,expr,pc)`.
* reducer: (list[T],T,list[T])->list[T] where T = (output,expr,pc) (default=None)
  - This function is used to reduce statements in a resulting summary.

##### Returns
* json_obj: dict[str:str] or dict[str:list[str]]
