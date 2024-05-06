from __future__ import annotations
from creature_combat.utils import annotations as anno


def clip(value: anno.Union[float, int], min_val: anno.Union[float, int], max_val: anno.Union[float, int]) -> anno.Union[float, int]:
    """Clips the value provided to be on the bound [min_val, max_val]. 

    Args:
        value (Union[float, int]): Value to clip
        min_val (Union[float, int]): Minimum bound that the value can have
        max_val (Union[float, int]): Maximum bound that the value can have

    Returns:
        Union[float, int]: Clipped value
    """
    return max(min_val, min(value, max_val))