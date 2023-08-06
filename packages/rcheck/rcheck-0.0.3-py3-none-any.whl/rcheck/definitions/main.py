from rcheck.definitions.ins import _InGroup
from rcheck.definitions.out import _Out
from rcheck.definitions.post_check import _PostGroup
from rcheck.definitions.pre_check import _PreGroup


class InputValues:
    def __init__(self, input_dict):
        for input_name, input_value in input_dict.items():
            setattr(self, input_name, input_value)


class Check:
    def __init__(
        self, run_fn, ins=None, pre_check=None, out=None, post_check=None, off=False
    ):
        self.run_fn = run_fn

        # check ins is dict of ...
        self.ins = _InGroup(ins)

        self.pre_check = _PreGroup(pre_check)
        self.out = _Out(out)
        self.post_check = _PostGroup(post_check)
        self.off = off

    def __call__(self, *args, **kwargs):
        if self.off:
            return self.call_without_checking(*args, **kwargs)

        inputs_as_dict = kwargs

        self.ins.run_check(ins=inputs_as_dict)
        input_class = InputValues(kwargs)

        self.pre_check.run_check(input_class)

        result = self.run_fn(*args, **kwargs)
        self.out.run_check(result)

        self.post_check.run_check(input_class, result)

        return result

    def call_without_checking(self, *args, **kwargs):
        return self.run_fn(*args, **kwargs)
