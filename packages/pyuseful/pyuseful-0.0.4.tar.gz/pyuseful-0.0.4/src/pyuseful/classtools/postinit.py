# -----------------------------------------
# ------------Postinit---------------------
# -----------------------------------------
from typing import Tuple, Dict, Any
from abc import abstractmethod, ABCMeta

class PostInitMeta(ABCMeta):
    """Metaclass that adds a call to __postinit__ which is called after __init__"""
    def __call__(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        obj = type.__call__(cls, *args, **kwargs)
        obj.__postinit__()
        return obj
    

class PostInit(metaclass=PostInitMeta):
    """Base class that adds a call to __postinit__ which is called after __init__"""
    @abstractmethod
    def __postinit__(self) -> None:
        pass

# ==============================================


if __name__ == "__main__":
    pass