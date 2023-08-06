maintenance
===========

This library provides utilities to easily deprecate
code, without manually setting up the warnings.
If your project uses experimental feautures, this
library might be useful as well.


Installation
------------

```bash
pip install maintenance.py
```


Usage
-----

```python
from maintenance import deprecated, experimental

class MyClass:
    def matches_pep8_convention(self, arg):
        self.arg = arg
        print(arg)
    
    @deprecated(
        "New method matches pep8 convention.",
        new = "matches_pep8_convention",
        since = "1.2.3",
    )
    def doesNotMatchPep8Convention(self, arg):
        return self.matches_pep8_convention(arg)
    
    @experimental(
        "Can only be used when `matches_pep8_convention` was previously used.",
        stable_in = "2.0.0"
    )
    def might_break(self):
        print(self.arg)

```

Both functions `deprecated` and `experimental` only
have optional parameters.


Parameters for `deprecated`
---------------------------

message
> Optional message providing extra information.

new
> The new object, that is intended to use.
> May be a python object or a string.

since
> A version number since when this object
> is deprecated.


Parameters for `experimental`
-----------------------------

message
> Optional message providing extra information.

stable_in
> Version number, when the object is expected
> to be stable.
