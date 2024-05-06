from typing import Union


def clip(value: Union[float, int], min_val: Union[float, int], max_val: Union[float, int]) -> Union[float, int]:
    """Clips the value provided to be on the bound [min_val, max_val]. 

    Args:
        value (Union[float, int]): Value to clip
        min_val (Union[float, int]): Minimum bound that the value can have
        max_val (Union[float, int]): Maximum bound that the value can have

    Returns:
        Union[float, int]: Clipped value
    """
    return max(min_val, min(value, max_val))