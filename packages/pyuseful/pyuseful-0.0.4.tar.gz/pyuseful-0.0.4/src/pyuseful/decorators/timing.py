from functools import wraps
from typing import Callable, Tuple, Dict, Any
import time


def time_exec(_func=None, *, printout: bool = True) -> Callable:
    """Decorator factory, adds 'last_call_elapsed' and 'total_time' attributes to a fucntion

    Args:
        printout: bool, printout to console; default is True
    """
    def timing_base(fun: Callable) -> Callable:
        """decorator for timing"""
        @wraps(fun)
        def wrapper(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            start = time.time()
            result = fun(*args, **kwargs)
            end = time.time()
            elapsed = (end-start)*1000.0
            wrapper.last_call_elapsed = elapsed
            wrapper.total_time = wrapper.total_time + elapsed
            if printout:
                print(f'{fun.__name__:s} function took {elapsed:.3f} ms')
            return result

        wrapper.last_call_elapsed = 0
        wrapper.total_time = 0
        return wrapper
        

    if _func is None:
        return timing_base
    else:
        return timing_base(_func)

