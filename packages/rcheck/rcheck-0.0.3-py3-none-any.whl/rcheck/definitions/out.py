from typing import Callable

from rcheck.checks import assert_opt_str, assert_str


class InvalidOutType(Exception):
    ...


class CheckOut:
    def __init__(self, name, check_fn, description=None):
        assert_str(name, "name")
        assert_opt_str(description, "description")

        self.name = name
        self.check_fn = check_fn
        self.description = description

    def run_check(self, val):
        try:
            possible_bool_result = self.check_fn(val)

            if possible_bool_result is not None and possible_bool_result != True:
                raise InvalidOutType(
                    f"Failed running check '{self.name}'. Got value '{val}':{type(val).__name__}."
                )

        except Exception as check_error:
            raise


class _Out:
    def __init__(self, outs_dict):
        self.outs = []

        if outs_dict is None:
            return

        for check_name, out in outs_dict.items():
            if isinstance(out, Callable):
                self.outs.append(CheckOut(check_name, out))
            elif isinstance(out, CheckOut):
                self.outs.append(out)

    def run_check(self, out):
        for check_out in self.outs:
            check_out.run_check(out)
