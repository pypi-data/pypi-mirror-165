from datetime import date, datetime
from typing import Optional, Union

from rcheck.checks.shared import (
    InvalidRuntype,
    _assert_simple_type_fail_message,
    _isinstance,
)

#
# General condition
#


def _assert_true_fail_message(name: str, message: Optional[str] = None):
    return InvalidRuntype(f"Conditions not met for {name}." + (f"\n\n{message}" or ""))


def assert_cond(condition: bool, name: str, message: Optional[str] = None):
    if not condition:
        raise _assert_true_fail_message(name, message)


#
# bool
#


def is_bool(val: object):
    return _isinstance(val, bool)


def assert_bool(val: object, name: str, message: Optional[str] = None):
    if not is_bool(val):
        raise _assert_simple_type_fail_message("bool", val, name, message)


def is_opt_bool(val: object):
    return val is None or is_bool(val)


def assert_opt_bool(val: object, name: str, message: Optional[str] = None):
    if not is_opt_bool(val):
        raise _assert_simple_type_fail_message("Optional[bool]", val, name, message)


#
# str
#


def is_str(val: object):
    return _isinstance(val, str)


def assert_str(val: object, name: str, message: Optional[str] = None):
    if not is_str(val):
        raise _assert_simple_type_fail_message("str", val, name, message)


def is_opt_str(val: object):
    return val is None or is_str(val)


def assert_opt_str(val: object, name: str, message: Optional[str] = None):
    if not is_opt_str(val):
        raise _assert_simple_type_fail_message("Optional[str]", val, name, message)


#
# int
#


def is_int(val: object):
    return _isinstance(val, int)


def assert_int(val: object, name: str, message: Optional[str] = None):
    if not is_int(val):
        raise _assert_simple_type_fail_message("int", val, name, message)


def is_opt_int(val: object):
    return val is None or is_int(val)


def assert_opt_int(val: object, name: str, message: Optional[str] = None):
    if not is_opt_int(val):
        raise _assert_simple_type_fail_message("Optional[int]", val, name, message)


#
# float
#


def is_float(val: object):
    return _isinstance(val, float)


def assert_float(val: object, name: float, message: Optional[str] = None):
    if not is_float(val):
        raise _assert_simple_type_fail_message("float", val, name, message)


def is_opt_float(val: object):
    return val is None or is_float(val)


def assert_opt_float(val: object, name: float, message: Optional[str] = None):
    if not is_opt_float(val):
        raise _assert_simple_type_fail_message("Optional[float]", val, name, message)


#
# Numbers
#

Number = Union[float, int]


def is_number(val: object):
    return _isinstance(val, (float, int))


def assert_number(val: object, name: str, message: Optional[str] = None):
    if not is_number(val):
        raise _assert_simple_type_fail_message("Number", val, name, message)


def is_opt_number(val: object):
    return val is None or is_number(val)


def assert_opt_number(val: object, name: str, message: Optional[str] = None):
    if not is_opt_number(val):
        raise _assert_simple_type_fail_message("Optional[Number]", val, name, message)


Number = Union[int, float]


def assert_positive(number: Number, name: str, message: Optional[str] = None):
    if number <= 0:
        _message = message

        if message is not None:
            _message = f"Expected variable {name} to be positive. Got {number}."

        raise _assert_true_fail_message(name, _message)


def assert_negative(number: Number, name: str, message: Optional[str] = None):
    if number >= 0:
        _message = message

        if message is not None:
            _message = f"Expected variable {name} to be negative. Got {number}."

        raise _assert_true_fail_message(name, _message)


def assert_non_positive(number: Number, name: str, message: Optional[str] = None):
    if number > 0:
        _message = message

        if message is not None:
            _message = f"Expected variable {name} to be non-positive. Got {number}."

        raise _assert_true_fail_message(name, _message)


def assert_non_negative(number: Number, name: str, message: Optional[str] = None):
    if number < 0:
        _message = message

        if message is not None:
            _message = f"Expected variable {name} to be non-negative. Got {number}."

        raise _assert_true_fail_message(name, _message)


#
# class
#


def is_instance(val: object, cls: object):
    return _isinstance(val, cls)


def assert_instance(val: object, cls: object, name: str, message: Optional[str] = None):
    if not is_instance(val, cls):
        raise _assert_simple_type_fail_message(cls.__name__, val, name, message)


def is_opt_instance(val: object, cls: object):
    return val is None or is_instance(val, cls)


def assert_opt_instance(
    val: object, cls: object, name: str, message: Optional[str] = None
):
    if not is_opt_instance(val, cls):
        raise _assert_simple_type_fail_message(
            f"Optional[{cls.__name__}]", val, name, message
        )


#
# callable
#


def is_callable(val: object):
    return callable(val)


def assert_callable(val: object, name: str, message: Optional[str] = None):
    if not is_callable(val):
        raise _assert_simple_type_fail_message("Callable", val, name, message)


def is_opt_callable(val: object):
    return val is None or is_callable(val)


def assert_opt_callable(val: object, name: str, message: Optional[str] = None):
    if not is_opt_callable(val):
        raise _assert_simple_type_fail_message("Optional[Callable]", val, name, message)


#
# date
#


def is_date(val: object):
    return _isinstance(val, date)


def assert_date(val: object, name: str, message: Optional[str] = None):
    if not is_date(val):
        raise _assert_simple_type_fail_message("date", val, name, message)


def is_opt_date(val: object):
    return val is None or is_date(val)


def assert_opt_date(val: object, name: str, message: Optional[str] = None):
    if not is_opt_date(val):
        raise _assert_simple_type_fail_message("Optional[date]", val, name, message)


#
# datetime
#


def is_datetime(val: object):
    return _isinstance(val, datetime)


def assert_datetime(val: object, name: str, message: Optional[str] = None):
    if not is_datetime(val):
        raise _assert_simple_type_fail_message("datetime", val, name, message)


def is_opt_datetime(val: object):
    return val is None or is_datetime(val)


def assert_opt_datetime(val: object, name: str, message: Optional[str] = None):
    if not is_opt_datetime(val):
        raise _assert_simple_type_fail_message("Optional[datetime]", val, name, message)
