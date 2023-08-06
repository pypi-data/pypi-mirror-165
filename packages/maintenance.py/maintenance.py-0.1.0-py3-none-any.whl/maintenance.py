from __future__ import annotations

__all__ = [
    "Version",
    "deprecated",
    "experimental",
]

from functools import wraps
from typing import Any, Optional
import warnings

from packaging.version import Version


class ExperimentalWarning(UserWarning):
    """
    Warning for feautures that are unstable at this point.
    """

def deprecated(
    message: Optional[str] = None,
    *,
    new: Optional[Any] = None,
    since: Optional[Version, str] = None,
):
    """
    Highlight a function, class or any callable as
    deprecated.
    
    Parameters
    ----------
    message
        Optional message providing extra information.
    
    new
        The new object, that is intended to use.
        May be a python object or a string.
    
    since
        A version number since when this object
        is deprecated.
    
    Example
    -------
    from maintenance import deprecated
    from packaging.version import Version
    
    @deprecated()
    def might_be_buggy(arg):
        return 1 / arg
    
    """
    if not isinstance(new, str) and new is not None:
        new = new.__name__
    
    def decorator(obj):
        @wraps(obj)
        def wrapper(*args, **kwargs):
            warnings.warn("".join([
                f"{obj.__name__!r} is deprecated",
                f" since {since}" if since is not None else "",
                f"; use {new!r} instead" if new is not None else "",
                f": {message}" if message is not None else ".",
            ]), DeprecationWarning, stacklevel = 2)
            
            return obj(*args, **kwargs)
        return wrapper
    return decorator

def experimental(
    message: Optional[str] = None,
    *,
    stable_in: Optional[Version, str] = None,
):
    """
    Highlight a function, class or any callable as
    an experimental feauture.
    
    Parameters
    ----------
    message
        Optional message providing extra information.
    
    stable_in
        Version number, when the object is expected
        to be stable.
    
    Example
    -------
    from maintenance import experimental
    from packaging.version import Version
    
    @experimental(stable_in = Version("1.2.3b4"))
    def might_be_buggy(arg):
        return 1 / arg
    
    """
    def decorator(obj):
        @wraps(obj)
        def wrapper(*args, **kwargs):
            warnings.warn("".join([
                f"{obj.__name__!r} is an experimental feauture",
                f"and will be stable in {stable_in}" if stable_in is not None else "",
                f": {message}" if message is not None else ".",
            ]), ExperimentalWarning, stacklevel = 2)
            
            return obj(*args, **kwargs)
        return wrapper
    return decorator
