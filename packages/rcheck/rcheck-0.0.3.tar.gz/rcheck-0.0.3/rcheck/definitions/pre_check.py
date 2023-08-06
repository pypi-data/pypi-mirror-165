class FailedPreCheck(Exception):
    ...


class _PostCheck:
    def __init__(self, check_name, check_fn):
        self.check_name = check_name
        self.check_fn = check_fn

    def run_check(self, ins):
        try:
            possible_bool_result = self.check_fn(ins)

            if possible_bool_result is not None and possible_bool_result != True:
                raise FailedPreCheck(f"Failed running check '{self.check_name}'")

        except Exception as check_error:
            raise


class _PreGroup:
    def __init__(self, post_checks_dict):
        self.post_checks = []

        if post_checks_dict is None:
            return

        for param_name, _in in post_checks_dict.items():
            self.post_checks.append(_PostCheck(param_name, _in))

    def run_check(self, ins):
        for post_check in self.post_checks:
            post_check.run_check(ins)
