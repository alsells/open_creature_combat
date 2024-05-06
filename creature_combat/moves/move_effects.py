from creature_combat.utils.extended_enums import ExtendedEnum


#TODO: Remove emun for parser using the format MOVE_TYPE:VALUE
# For Status effects use 3 lrt code (ex brn, psn, etc.)
# Moved Environment effects to its own list in the Move, and run a similar parser there
class MoveEffectEnum(ExtendedEnum):
    DAMAGE:int=0
    RAISE_P_ATK_1:int=1
    RAISE_P_ATK_2:int=2
    RAISE_P_ATK_3:int=3
    RAISE_P_DEF_1:int=4
    RAISE_P_DEF_2:int=5
    RAISE_P_DEF_3:int=6
    RAISE_S_ATK_1:int=7
    RAISE_S_ATK_2:int=8
    RAISE_S_ATK_3:int=9
    RAISE_S_DEF_1:int=10
    RAISE_S_DEF_2:int=11
    RAISE_S_DEF_3:int=12
    RAISE_SPD_1:int=13
    RAISE_SPD_2:int=14
    RAISE_SPD_3:int=15
    RAISE_ACC_1:int=16
    RAISE_ACC_2:int=17
    RAISE_ACC_3:int=18
    RAISE_EVA_1:int=19
    RAISE_EVA_2:int=20
    RAISE_EVA_3:int=21
    RAISE_CRIT_1:int=22
    RAISE_CRIT_2:int=23
    RAISE_CRIT_3:int=24
    LOWER_P_ATK_1:int=25
    LOWER_P_ATK_2:int=26
    LOWER_P_ATK_3:int=27
    LOWER_P_DEF_1:int=28
    LOWER_P_DEF_2:int=29
    LOWER_P_DEF_3:int=30
    LOWER_S_ATK_1:int=31
    LOWER_S_ATK_2:int=32
    LOWER_S_ATK_3:int=33
    LOWER_S_DEF_1:int=34
    LOWER_S_DEF_2:int=35
    LOWER_S_DEF_3:int=36
    LOWER_SPD_1:int=37
    LOWER_SPD_2:int=38
    LOWER_SPD_3:int=39
    LOWER_ACC_1:int=40
    LOWER_ACC_2:int=41
    LOWER_ACC_3:int=42
    LOWER_EVA_1:int=43
    LOWER_EVA_2:int=44
    LOWER_EVA_3:int=45
    SUNLIGHT:int=46
    RAIN:int=47
    SANDSTORM:int=48
    SNOW:int=49
    FOG:int=50
    BURN:int=51
    FREEZE:int=52
    PARALYSIS:int=53
    POISON:int=54
    BADLY_POISONED:int=55
    SLEEP:int=56