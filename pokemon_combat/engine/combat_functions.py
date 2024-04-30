from numpy.random import randint, uniform
from pokemon_combat.engine.participant import Participant
from pokemon_combat.moves.move import Move
from pokemon_combat.moves.move_types import MoveTypeEnum
from pokemon_combat.utils.math_utils import clip
from pokemon_combat.utils.mappings import DAMAGE_MAP


def does_hit(move: Move, attacker: Participant, defender: Participant) -> bool:
    modifier = clip(attacker.acc_stage - defender.eva_stage, -6, 6)
    # Factor moves on a scale of 9/3 when modifier is 6, to 3/9 when modifier is -6. 
    factor = (3 + modifier) / 3 if modifier >= 0 else 3 / (3 - modifier)
    return randint(0, 100) <= int(move.accuracy * factor)


def does_crit(move: Move, attacker: Participant) -> bool:
    modifier = clip(int(move.high_crit_flag) + attacker.crit_stage, 0, 3)
    match modifier:
        case 0:
            target = 1/16
        case 1:
            target = 1/8
        case 2:
            target = 1/2
        case 3:
            target = 1.0
        case _:
            raise ValueError(f"Modifier went outside of allowable bounds [0-3] @ {modifier}. Plz fix.")
    return uniform(0.0, 1.0) <= target


def stat_stage_modifier(stage: int) -> float:
    stage = clip(stage, -6, 6)
    return (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)


def get_type_modifier(move: Move, target: Participant) -> float:
    mod = 1.0
    for target_type in target.pokemon._types:
        if target_type is not None:
            mod *= DAMAGE_MAP[move.element.value, target_type.value]
    return mod



def calculate_damge(move: Move, attacker: Participant, defender: Participant) -> int:
    match move.move_type:
        case MoveTypeEnum.PHYSICAL:
            a = attacker.p_atk * stat_stage_modifier(attacker.p_atk_stage)
            d = defender.p_def * stat_stage_modifier(defender.p_def_stage)
        case MoveTypeEnum.SPECIAL:
            a = attacker.s_atk * stat_stage_modifier(attacker.s_atk_stage)
            d = defender.s_def * stat_stage_modifier(defender.s_def_stage)
        case _:
            a = 0
            d = 0
    if a == 0 and d == 0:
        return 0
    stab = 1.5 if attacker.pokemon.is_stab(move) else 1.0
    power = move.power * stab
    base = ((2 * attacker.lvl) / 5 + 2) * power * (a / d) / 50 + 2
    crit = 1.5 if does_crit(move, attacker) else 1.0
    random = randint(85, 101) / 100
    type_modifier = get_type_modifier(move, defender)
    return int(base * crit * random * type_modifier)


def plarticipant_1_first(participant1: Participant, move1: Move, participant2: Participant, move2: Move) -> bool:
    if move1.priority > move2.priority:
        return True
    elif move1.priority < move2.priority:
        return False
    else:
        return participant1.spd * stat_stage_modifier(participant1.spd_stage) >= participant2.spd * stat_stage_modifier(participant2.spd_stage)


def apply_status(effect_name: str, attacker: Participant, defender: Participant, self: bool) -> None:
    modifier, stat, ammount = effect_name.split('_')
    effected = attacker if self else defender
    match modifier:
        case "RAISE":
            mod = 1
        case "LOWER":
            mod = -1
        case _:
            raise ValueError(f"Stat stage change move effect modifier was provided as {modifier} and not [RAISE or LOWER]")
    ammount *= mod
    match stat:
        case "PATK":
            effected.adjust_p_atk_stage(ammount)
        case "PDEF":
            effected.adjust_p_def_stage(ammount)
        case "SATK":
            effected.adjust_s_atk_stage(ammount)
        case "SDEF":
            effected.adjust_s_def_stage(ammount)
        case "SPD":
            effected.adjust_spd_stage(ammount)
        case "ACC":
            effected.adjust_acc_stage(ammount)
        case "EVA":
            effected.adjust_eva_stage(ammount)
        case "CRIT":
            effected.adjust_crit_stage(ammount)
        case _:
            raise ValueError(f"Unable to parse stat change category {stat}, please provide a valid stat category.")