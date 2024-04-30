from typing import Union

def clip(value: Union[float, int], min_val: Union[float, int], max_val: Union[float, int]) -> Union[float, int]:
    return max(min_val, min(value, max_val))