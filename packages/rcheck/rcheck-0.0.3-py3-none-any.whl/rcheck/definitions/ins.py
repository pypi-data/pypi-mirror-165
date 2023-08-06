from typing import Callable

from ..checks import assert_str


class InvalidArgumentType(Exception):
    ...


class CheckIn:
    def __init__(self, name, check_fn, description=None, param_name=None):
        assert_str(name, "CheckIn.__init__:name")
        assert_str(name, "CheckIn.__init__:description")

        self.name = name
        self.check_fn = check_fn
        self.description = description
        self.param_name = param_name

    def add_param_name(self, param_name: str):
        self.param_name = param_name

    def run_check(self, val):
        try:
            possible_bool_result = self.check_fn(val)

            if possible_bool_result is not None and possible_bool_result != True:
                raise InvalidArgumentType(
                    f"Failed running check '{self.name}' for parameter '{self.param_name}'. Got value '{val}'."
                )

        except Exception as check_error:
            raise


class _In:
    def __init__(self, param_name, checks):
        self.param_name = param_name
        self.check_ins = []

        if isinstance(checks, Callable):
            self.check_ins.append(
                CheckIn(
                    name=f"Check {param_name}", check_fn=checks, param_name=param_name
                )
            )
        elif isinstance(checks, CheckIn):
            self.check_ins.append(checks)
        elif isinstance(checks, dict):
            for check_name, check in checks.items():
                self.check_ins.append(
                    CheckIn(name=check_name, check_fn=check, param_name=param_name)
                )
        elif isinstance(checks, list):
            for check in checks:
                if not isinstance(check, CheckIn):
                    raise Exception()

    def run_check(self, val):
        for check_in in self.check_ins:
            check_in.run_check(val)


class _InGroup:
    def __init__(self, ins_dict):
        self.ins = []

        if ins_dict is None:
            return

        for param_name, _in in ins_dict.items():
            self.ins.append(_In(param_name, _in))

    def run_check(self, ins):
        for check_in in self.ins:
            check_in.run_check(ins[check_in.param_name])
