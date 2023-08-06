from typing import Optional

from rcheck.checks.basic_types import _assert_simple_type_fail_message
from rcheck.checks.shared import InvalidRuntype, _isinstance

#
# list
#


def _assert_list_type_fail_message(
    expected_type_str: str,
    val: object,
    name: str,
    failure_index: int,
    message: Optional[str] = None,
):
    return InvalidRuntype(
        f"Expected list items of {name} to be type {expected_type_str}. "
        + f"Got value {val!r} of type {type(val).__name__} at index {failure_index}."
        + (f"\n\n{message}" or "")
    )


def _is_iterable_of(iterable, sub_type):
    for idx, item in enumerate(iterable):
        if not _isinstance(item, sub_type):
            return False, idx

    return True, -1


def is_list(val: object, of: Optional[type] = None):
    if not _isinstance(val, list):
        return False

    return True if of is None else _is_iterable_of(val, of)[0]


def assert_list(
    val: object,
    name: str,
    message: Optional[str] = None,
    *,
    of: Optional[type] = None,
):
    if not _isinstance(val, list):
        raise _assert_simple_type_fail_message("list", val, name, message)

    if of is None:
        return

    items_pass_check, failed_idx = _is_iterable_of(val, of)
    if not items_pass_check:
        raise _assert_list_type_fail_message(
            of.__name__, val[failed_idx], name, failed_idx, message
        )


def _is_iterable_of_opt(iterable, sub_type):
    for idx, item in enumerate(iterable):
        if item is not None and not _isinstance(item, sub_type):
            return False, idx

    return True, -1


def is_list_of_opt(val: object, of_optional: type):
    if not _isinstance(val, list):
        return False

    return _is_iterable_of_opt(val, of_optional)[0]


def assert_list_of_opt(
    val: object,
    of_optional: type,
    name: str,
    message: Optional[str] = None,
):
    if not _isinstance(val, list):
        raise _assert_simple_type_fail_message("list", val, name, message)

    if of_optional is None:
        return

    items_pass_check, failed_idx = _is_iterable_of_opt(val, of_optional)
    if not items_pass_check:
        raise _assert_list_type_fail_message(
            of_optional.__name__, val[failed_idx], name, failed_idx, message
        )


def is_opt_list(val: object, of: Optional[type] = None):
    return val is None or is_list(val, of)


def assert_opt_list(
    val: object,
    name: str,
    message: Optional[str] = None,
    *,
    of: Optional[type] = None,
):
    if val is None:
        return

    if not _isinstance(val, list):
        raise _assert_simple_type_fail_message("list", val, name, message)

    if of is None:
        return

    items_pass_check, failed_idx = _is_iterable_of(val, of)
    if not items_pass_check:
        raise _assert_list_type_fail_message(
            of.__name__, val[failed_idx], name, failed_idx, message
        )


#
# dict
#
