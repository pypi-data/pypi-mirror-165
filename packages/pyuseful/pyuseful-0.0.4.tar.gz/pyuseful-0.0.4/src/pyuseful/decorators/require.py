# -----------------------------------------
# ------------Require decorator factory----
# -----------------------------------------
from functools import wraps
from typing import Callable, Type, Tuple, Dict, Any, Optional


def _mangle_args(self: Type[object], inp: str) -> str:
    """Mangle names starting with 'self.__'

    Args:
        self: subclass of object
        inp: str, contains valuate expression
    """
    return inp.replace("self.__", f"self._{_cls_name(self)}__")

def _mangle_single(self: Type[object], inp: str) -> str:
    """Mangle names starting with '__'
    
    Args:
        self: subclass of object
        inp: str, contains name of an object attribute
    """
    return inp.replace("__", f"_{_cls_name(self)}__") if inp.find("__") == 0 else inp

def _cls_name(obj: Type[object]) -> str:
    return obj.__class__.__name__
# -----------------------------------------
# -----------------------------------------

def require_condition(var: Optional[str] = None, cond: Optional[str] = None, msg: Optional[str] = None) -> Callable:
    """Decorator factory for requiring a condition to be True, if 'cond' is None evaluate 'var' alone
    
    Args:
        var: str, argument name is a class
        cond: str, evaluate condition used by eval(), left side is a value of 'var'
        msg: str, display on error
    """
    if var is None and cond is None:
        raise ValueError("at least one argument must be provided: 'var', 'cond'")

    for x in (var, cond, msg):
        if x is not None and not isinstance(x, str):
            raise TypeError(f"argument '{x}' must be str")


    cond_str = cond if cond is not None else ""
    var_str = f"self.{var}" if var is not None else ""
    msg = msg if msg else f"'{var_str}{cond_str}' must evaluate to 'True'"

    def require_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: Type[object], *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            nonlocal cond, var
            cond = _mangle_args(self, cond) if cond is not None else None
            var = _mangle_single(self, var) if var is not None else None

            try:
                value = self.__dict__[var] if var is not None else ""
            except KeyError:
                raise AttributeError(f"'{_cls_name(self)}' object has no attribute '{var}'") 

            condition = eval(f"{value}{cond}") if cond is not None else bool(value)
            if not condition:
                raise RuntimeError(msg)
                
            return func(self, *args, **kwargs)

        return wrapper

    return require_decorator

# -----------------------------------------
# -----------------------------------------

def once(_func=None, *, mode="cashed"):
    """Decorator to allow a function to only be called once or
     always return result of the 1st call
    
    Args:
        mode: str, 'cashed' - always return 1st result, 
        'error' - raise an error if called a 2nd time
    """
    if mode not in ("cashed", "error"):
        raise ValueError("'mode' argument can only be: 'cashed' or 'error'")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not wrapper._done:
                wrapper._cashed_result = func(*args, **kwargs)
                wrapper._done = True
            elif mode == "error":
                raise RuntimeError(f"'{func.__name__}' can only be called once")
            return wrapper._cashed_result

        wrapper._cashed_result = None   
        wrapper._done = False
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

# -----------------------------------------
# -----------------------------------------

def limit(max_calls):
    """Decorator to allow a function to only be called 
    'max_calls' amount of times
    
    Args:
        max_calls: int, how many time a function can be called 
    """
    if not isinstance(max_calls, int):
        raise TypeError("'max_calls' must be int")
    if max_calls < 1:
        raise ValueError("'max_calls' must be greater than 0")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._calls += 1
            if wrapper._calls > max_calls:
                raise RuntimeError(f"'{func.__name__}' can only be called {max_calls} times")
            return func(*args, **kwargs)

        wrapper._calls = 0   
        return wrapper

    return decorator

if __name__ == "__main__":
    pass