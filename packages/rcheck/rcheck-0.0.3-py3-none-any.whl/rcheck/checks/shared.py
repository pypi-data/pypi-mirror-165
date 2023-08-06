from typing import Optional, Tuple, Union


class InvalidRuntype(Exception):
    ...


def _assert_simple_type_fail_message(
    expected_type_str: str, val: object, name: str, message: Optional[str] = None
):
    return InvalidRuntype(
        f"Expected variable {name} to be type {expected_type_str}. "
        + f"Got value {val!r} of type {type(val).__name__}. "
        + (message or "")
    )


TypeOrTuple = Union[type, Tuple[type, ...]]


def _isinstance(val: object, _type: TypeOrTuple):
    # Boolean values are instance of ints for python backwards compatability reasons
    # This behavior is not supported in this library
    if isinstance(val, bool) and (
        _type == int
        or (isinstance(_type, tuple) and int in _type and bool not in _type)
    ):
        return False

    return isinstance(val, _type)
