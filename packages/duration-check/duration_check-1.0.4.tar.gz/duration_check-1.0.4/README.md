# [Duration Check](https://pypi.org/project/duration-check/)
Working python decorators to check how long function can take to be executed.


## Decorator available
 - `timeout` via `timeout_decorator_builder()`
 - `duration`

## Code example
```python
import sys
import unittest

from duration_check import timeout_decorator_builder

# This CAN NOT be a lambda function because we can't pickle them
def module_getter():
    return sys.modules[__name__]

timeout = timeout_decorator_builder(module_getter)  # This CAN NOT be a lambda function because we can't pickle them

class SuperTaskUnitTest(unittest.TestCase):

    @timeout(2)
    def test_timeout_super_task(self):
        self.assertTrue(my_super_task())
```
## Issues/Bug report or improvement ideas
https://gitlab.com/devolive/pypi-packages/duration-check/-/issues

## License
GNU Lesser General Public License v3 or later (LGPLv3+)
