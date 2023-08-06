# `rcheck`

Runtime type checking.

---

Functions that return a boolean:
* `is_<type>` such as `is_int`, `is_bool`, etc...
* `is_opt_<type>` such as `is_opt_int`, `is_opt_bool`, etc.. for optional types

Functions that raise exceptions:
* `assert_<type>` such as `assert_int`, `assert_bool`, etc...
* `assert_opt_<type>` such as `assert_opt_int`, `assert_opt_bool`, etc... for optional types

Function parameter checking:
```python
from rcheck import check, is_datetime

@check(
    ins={
        "start_date": is_datetime,
        "middle_date": is_datetime,
    },
    pre_check={
        "Middle date comes after start date": lambda ins: ins.start_date < ins.middle_date
    }
)
def get_next_date(start_date, middle_date):
    return middle_date + (middle_date - start_date)

get_next_date(datetime(2022, 2, 1), datetime(2022, 1, 1))

>>> FailedPreCheck: Failed running check 'Middle date comes after start date'
```
