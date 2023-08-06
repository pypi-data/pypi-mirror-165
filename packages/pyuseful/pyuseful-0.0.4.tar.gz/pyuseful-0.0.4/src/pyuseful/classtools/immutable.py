# -----------------------------------------
# ------------Immutable properties---------
# -----------------------------------------
from typing import Any, Type
class PropertyImmutable(Exception):
    """Cannot mutate an already set property"""
    pass

def _cls_name(obj: Type[object]) -> str:
    return obj.__class__.__name__
    
class ImmutableProperties():
    """Immutable properties in class except with prefixes defined in 'mut_prefix'"""

    mut_prefix = ("__", )

    def __setattr__(self, name: str, value: Any) -> None:
        """After the value is set to not None it cannot be changed"""
        cls = type(self)
        mangle = lambda x: f"_{_cls_name(self)}{x}" if x.startswith("__") else x

        if cls.mut_prefix:
            is_mut = any([name.startswith(mangle(t)) for t in cls.mut_prefix])
        else:
            is_mut = False

        if not is_mut:
            try:
                current_value = self.__dict__[name]
            except:
                current_value = None
            if name in self.__dict__ and current_value is not None:
                raise PropertyImmutable(f"Property '{name}' in '{_cls_name(self)}' is immutable")
        self.__dict__[name] = value

if __name__ == "__main__":
    pass