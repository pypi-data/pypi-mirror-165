from typing import Optional

from .checks import assert_opt_bool
from .definitions import Check


def check(
    run_fn=None,
    *,
    ins=None,
    pre_check=None,
    out=None,
    post_check=None,
    off: Optional[bool] = None
):
    """

    Params
    ------
    run_fn
    ins
    pre_check
    out
    post_check

    """

    # If this function is used:
    #
    #   1. Without passing in any arguments. E.g.:
    #      >>> @check
    #      ... def some_func():
    #      ...     ...
    #
    #   2. Not as a decorator function. E.g.:
    #      >>> check(some_func, ...)
    #

    if run_fn is not None:
        fn_name = ...

        assert_opt_bool(off, "off")

        if ins is None:
            # ins from signature typing
            ...

        if out is None:
            # out from signature typing
            ...

        return Check(
            run_fn=run_fn,
            ins=ins,
            pre_check=pre_check,
            out=out,
            post_check=post_check,
            off=off,
        )

    # If this function is used as a decorator with arguments:
    #
    # E.g:
    # >>> @check(ins=..., ...)
    # ... def some_func():
    # ...     ...
    def _check(run_fn):
        return check(
            run_fn,
            ins=ins,
            pre_check=pre_check,
            out=out,
            post_check=post_check,
            off=off,
        )

    return _check
