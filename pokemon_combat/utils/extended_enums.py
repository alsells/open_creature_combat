from enum import Enum
from typing import Union
from typing_extensions import Self

class ExtendedEnum(Enum):
    @classmethod
    def init_from_key_or_value(cls, init_object: Union[str, int]) -> Self:
        if isinstance(init_object, str):
            return cls[init_object]
        elif isinstance(init_object, int):
            return cls(init_object)
        else:
            raise RuntimeError(f"Could not initialize {cls} with input {init_object}. Provide either a valid string or int.")