from creature_combat.utils.extended_enums import ExtendedEnum


class NonVolatileStatusEnum(ExtendedEnum):
    NONE: int=-1
    BRN:int=0
    FRZ:int=1
    PAR:int=2
    PSN:int=3
    BPSN:int=4
    SLP:int=5