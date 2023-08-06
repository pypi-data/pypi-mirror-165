from .postinit import PostInit

from abc import abstractclassmethod, abstractmethod
from typing import Tuple, Dict, Any, List, Type, Optional
import json

class PropertyMissing(Exception):
    """All required properties must be set"""
    pass


class TooManyProperties(Exception):
    """Too many properties in 'require_any'"""
    pass


def _cls_name(obj: Type[object]) -> str:
    return obj.__class__.__name__

# -----------------------------------------
# -----------------------------------------
class RequireAttrs(PostInit):
    """Require an object to have a list of required attributes after init"""
    @property
    @abstractclassmethod
    def require(self) -> Tuple[str, ...]:
        """This will require you to set attributes a and b
           
            Usage:

                require = ('a', 'b')
        """
        pass

    def __postinit__(self) -> None:
        """Check if every required arg is set"""
        for arg in self.require:
            if arg not in self.__dict__:
                raise PropertyMissing(
                    f"'{_cls_name(self)}' is missing attribute '{arg}'")
            if self.__dict__[arg] is None:
                raise PropertyMissing(
                    f"'{_cls_name(self)}' attribute '{arg}' must be not None")

# -----------------------------------------
# -----------------------------------------
class RequireDictParser(RequireAttrs):
    """Parse dict with required parameters, requires declaration 
    of 'require' and 'require_any' class attributes. Class attribute 
    'infer_numbers' sets if number strings will be convreted to numbers
    """

    infer_numbers = True
    
    @property
    @abstractclassmethod
    def require_any(self) -> Optional[Tuple[Tuple[Tuple[str, ...], int], ...]]:
        """This will require you to set attributes either a or b, 
        and either x & y or x & z or y & z

            Usage:

                require_any = (
                    (("a", "b"), 1),
                    (("x", "y", "z"), 2)
                )
        """
        pass

    @abstractmethod
    def declare_args(self) -> None:
        """ Typing the attributes or setting init values as 'None',
        will raise an error on trying to set a different value
        """
        pass

    @abstractmethod
    def set_args(self) -> None:
        """Set all missing properties from 'require_any' here"""
        pass

    @classmethod
    def from_json(cls, filename: str, encoding: str = "utf-8"):
        with open(filename, "r", encoding=encoding) as json_file:
            data = json.load(json_file)
        return cls(data)

    def __init__(self, import_data: Dict) -> None:
        if not isinstance(import_data, dict):
            raise AttributeError(
                f"'import_data' in {_cls_name(self)} must be a dict")

        self._declaring = True
        self.declare_args()
        self._declaring = False

        if self.require_any:
            for keys, amount in self.require_any:
                self._check_require_set(keys, amount, import_data)
                if len(keys) <= amount:
                    raise TooManyProperties(
                        f"'{_cls_name(self)}': Too many required properties in 'import_data': {amount} in {keys}, max is {len(keys)-1}")

        for key in self.require:
            if key not in import_data:
                raise PropertyMissing(f"'{_cls_name(self)}': Missing property {key} in 'import_data'")

        for key, item in import_data.items():
            if isinstance(item, str) and type(self).infer_numbers:
                try:
                    self.__dict__[key] = int(item)
                except ValueError:
                    try:
                        self.__dict__[key] = float(item)
                    except ValueError:
                        self.__dict__[key] = item
            else:
                self.__dict__[key] = item

        self.set_args()

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            declaring = self._declaring
        except AttributeError:
            declaring = False

        if declaring and (value is not None) and name != "_declaring":
            raise AttributeError(f"'{_cls_name(self)}': can only set values to 'None' in `declare_args` ({name}={value})")
            
        super().__setattr__(name, value)

    def __postinit__(self):
        """Check if every required arg is set"""
        super().__postinit__()

        for arg in self._required_any_keys:
            if arg not in self.__dict__:
                raise PropertyMissing(
                    f"'{_cls_name(self)}' is missing attribute '{arg}'")

            if self.__dict__[arg] is None:
                raise PropertyMissing(
                    f"'{_cls_name(self)}' attribute '{arg}' must be not None")

    @property
    def _required_any_keys(self):
        """Returns all property keys in require_any"""
        if self.require_any:
            return [y for x in self.require_any for y in x[0]]
        else:
            return []

    def _check_require_set(self, keys: List, amount: int, import_data: Dict):
        """Checks if data contains correct combination of keys from require_any"""
        if amount < 1:
            raise AttributeError(f"'{_cls_name(self)}': amount of properties for {keys} must be greater or equal to 1")

        found = 0
        for key in keys:
            if key in import_data:
                found += 1

        if not found:
            raise PropertyMissing(f"'{_cls_name(self)}': Missing one of the properties from {keys} in 'import_data'")

        if found > amount:
            raise TooManyProperties(
                f"'{_cls_name(self)}': The required amount of properties in {keys} is {amount} but {found} was found in 'import_data'")
