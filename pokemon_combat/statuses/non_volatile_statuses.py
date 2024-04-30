from pokemon_combat.utils.extended_enums import ExtendedEnum


class NonVolatileStatusEnum(ExtendedEnum):
    NONE: int=-1
    BURNED:int=0
    FROZEN:int=1
    PARALYZED:int=2
    POISONED:int=3
    BADLY_POISONED:int=4
    SLEEPING:int=5