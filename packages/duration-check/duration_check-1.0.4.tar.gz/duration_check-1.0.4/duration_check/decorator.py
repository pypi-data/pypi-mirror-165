import unittest

from types import ModuleType
from typing import Callable, Union, Optional
from multiprocessing import Process
from datetime import datetime

from .exception import TimeoutOccurred, MinimalDurationNotRespected


MODULE_GETTER_TYPE = Callable[[], ModuleType]
PREFIX = "__duration_check_decorator_"


def _format_datetime(datetime_):
    return f"{datetime_.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"


def _register_original_timeout_function(func, module_getter: MODULE_GETTER_TYPE, logging: bool):
    new_qualname = PREFIX + func.__qualname__
    if logging:
        print(f"Registering function '{func.__qualname__}' under '{new_qualname}'")
    setattr(module_getter(), new_qualname, func)
    # func.__qualname__ = new_qualname
    return new_qualname


def _timeout_process(module_getter: MODULE_GETTER_TYPE,
                     updated_qualname: str,
                     self_qualname: Optional[str],
                     verbose: bool,
                     *args, **kwargs):

    if self_qualname is not None:
        # The function is a method, so we get back the class instance.
        # Only work in the class is a singleton
        clazz = getattr(module_getter(), self_qualname)
        method_self = clazz()
        args = (method_self, *args)

    # Get the function with the previously updated qualname
    function = getattr(module_getter(), updated_qualname)

    starting_datetime = None
    if verbose:
        starting_datetime = datetime.utcnow()
        print(f"Entering function '{updated_qualname[len(PREFIX):]}' at {_format_datetime(starting_datetime)}")

    result = function(*args, **kwargs)

    if verbose:
        ending_datetime = datetime.utcnow()
        print(f"Leaving function '{updated_qualname[len(PREFIX):]}' at {_format_datetime(ending_datetime)}",
              f"(elapsed time: {ending_datetime - starting_datetime})")
    return result


def _is_a_method(args, decorated_function):
    return len(args) >= 1 and hasattr(args[0], decorated_function.__name__)


def _is_unittest_test_case(object_):
    return isinstance(object_, unittest.TestCase)


def timeout_decorator_builder(module_getter: MODULE_GETTER_TYPE,
                              default_verbose: bool = False,
                              register_logging: bool = False):

    def timeout_decorator(max_second_allowed: Union[int, float], verbose: bool = default_verbose):

        def _timeout_decorator_inner(decorated_function):
            new_qualname = _register_original_timeout_function(decorated_function, module_getter, register_logging)

            def _timeout_decorator_wrapper(*args, **kwargs):
                method_self = None
                if _is_a_method(args, decorated_function):
                    # This is a method
                    method_self = args[0]
                    args = (module_getter, new_qualname, method_self.__class__.__qualname__, verbose, *args[1:])
                else:
                    # This is a function
                    args = (module_getter, new_qualname, None, verbose, *args)

                process = Process(target=_timeout_process, args=args, kwargs=kwargs)
                process.start()
                # This is faster than time.sleep(),
                # as it'll exit early if the function finishes early.
                process.join(max_second_allowed)
                done_in_time = not process.is_alive()
                if not done_in_time:
                    process.terminate()
                if method_self is not None and _is_unittest_test_case(method_self):
                    method_self.assertTrue(done_in_time, f"Function ran out out time: {max_second_allowed} second(s)")
                else:
                    raise TimeoutOccurred(max_second_allowed, new_qualname)
            return _timeout_decorator_wrapper
        return _timeout_decorator_inner
    return timeout_decorator


def duration_decorator_builder(default_verbose: bool = False,
                               exception_raised: Optional[type(Exception)] = MinimalDurationNotRespected):

    def duration_decorator(min_second_allowed: Union[int, float], verbose: bool = default_verbose):
        def _duration_decorator_inner(decorated_function):
            def _duration_decorator_wrapper(*args, **kwargs):

                starting_datetime = datetime.utcnow()
                if verbose:
                    print(f"Entering function '{decorated_function.__qualname__}' at " +
                          f"{_format_datetime(starting_datetime)}")

                result = decorated_function(*args, **kwargs)
                ending_datetime = datetime.utcnow()

                if verbose:
                    print(f"Leaving function '{decorated_function.__qualname__}' at " +
                          f"{_format_datetime(ending_datetime)} (elapsed time: {ending_datetime - starting_datetime})")

                duration_respected = (ending_datetime - starting_datetime).total_seconds() > min_second_allowed
                if _is_a_method(args, decorated_function) and _is_unittest_test_case(args[0]):
                    args[0].assertTrue(duration_respected, f"Function processed to fast: {min_second_allowed}" +
                                       " second(s) minimal is required")
                if exception_raised is not None and not duration_respected:
                    raise exception_raised(min_second_allowed)

                return result

            return _duration_decorator_wrapper
        return _duration_decorator_inner
    return duration_decorator


duration = duration_decorator_builder()
