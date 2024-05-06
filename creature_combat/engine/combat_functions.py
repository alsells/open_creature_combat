from numpy.random import randint, uniform, normal
from creature_combat.engine.participant import Participant
from creature_combat.moves.move import Move
from creature_combat.moves.move_types import MoveTypeEnum
from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
from creature_combat.utils.math_utils import clip
from creature_combat.utils.mappings import DAMAGE_MAP


def does_hit(move: Move, attacker: Participant, defender: Participant) -> bool:
    """Determines if the move from the attacker will hit the defender.

    Args:
        move (Move): The move the attacker is using 
        attacker (Participant): The attacker making the attack
        defender (Participant): The defender receiving the attack

    Returns:
        bool: Does the Move hit or not 
    """
    modifier = clip(attacker.acc_stage - defender.eva_stage, -6, 6)
    # Factor moves on a scale of 9/3 when modifier is 6, to 3/9 when modifier is -6. 
    factor = (3 + modifier) / 3 if modifier >= 0 else 3 / (3 - modifier)
    return randint(0, 100) <= int(move.accuracy * factor)


def does_crit(move: Move, attacker: Participant) -> bool:
    """Determines if the move will crit on the target or not.

    Args:
        move (Move): The move being used by the attacker
        attacker (Participant): The attacker using the move

    Raises:
        ValueError: If the crit_stage of the attacker is beyond the expected range of [0-3] something critically has gone wrong and will error out.

    Returns:
        bool: Does the move crit the target or not 
    """
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
    """Gets the damage modifier for the move against the target based on the typing of both the target and move.

    Args:
        move (Move): Move being used against the target
        target (Participant): Target being attacked by the move

    Returns:
        float: How much the damage is modified based on the typing between the move and target
    """
    mod = 1.0
    for target_type in target.creature._types:
        if target_type is not None:
            mod *= DAMAGE_MAP[move.element.value, target_type.value]
    return mod


def calculate_damage(move: Move, attacker: Participant, defender: Participant) -> int:
    """Determines how much damage is done by the move from the attacker to the defender. The function follows a simplified version of the GEN5+ damage calculation formula found here: https://bulbapedia.bulbagarden.net/wiki/Damage

    Args:
        move (Move): The move being used by the attacker
        attacker (Participant): The attacker using the attack
        defender (Participant): The defender receiving the attack

    Returns:
        int: How much damage should be dealt to the defender 
    """
    match move.move_type:
        case MoveTypeEnum.PHYSICAL:
            a = attacker.p_atk
            d = defender.p_def
        case MoveTypeEnum.SPECIAL:
            a = attacker.s_atk
            d = defender.s_def
        case _:
            a = 0
            d = 0
    if a == 0 and d == 0:
        return 0
    stab = 1.5 if attacker.creature.is_stab(move) else 1.0
    power = move.power * stab
    base = ((2 * attacker.lvl) / 5 + 2) * power * (a / d) / 50 + 2
    crit = 1.5 if does_crit(move, attacker) else 1.0
    random = randint(85, 101) / 100
    type_modifier = get_type_modifier(move, defender)
    return int(base * crit * random * type_modifier)


def participant_1_first(participant1: Participant, move1: Move, participant2: Participant, move2: Move) -> bool:
    """Determines who between participant 1 and 2 should go first. Will first check the move priority of the moves that they are using, and if they are tied, 
    use the participants speed as a tie breaker, with Priority given to Participant 1.

    Args:
        participant1 (Participant): Participant 1 in the round 
        move1 (Move): Move used by participant 1
        participant2 (Participant): Participant 2 in the round
        move2 (Move): Move used by participant 2

    Returns:
        bool: Does participant 1 go for or does participant 2 go first
    """
    if move1.priority > move2.priority:
        return True
    elif move1.priority < move2.priority:
        return False
    else:
        return participant1.spd >= participant2.spd


def adjust_stat_stage(effect_name: str, effected: Participant) -> None:
    """Parses the effect name and adjusts the effected participants stat stage based on the name.

    Args:
        effect_name (str): Name of the effect effecting the participant
        effected (Participant): Participant the effect applies to

    Raises:
        ValueError: If a non stat effect is passed in, it can not be parsed to adjust a specific stat and will error out.
    """
    stat, amount  = effect_name.split(':')
    amount = int(amount)
    match stat:
        case "P_ATK":
            effected.adjust_p_atk_stage(amount)
        case "P_DEF":
            effected.adjust_p_def_stage(amount)
        case "S_ATK":
            effected.adjust_s_atk_stage(amount)
        case "S_DEF":
            effected.adjust_s_def_stage(amount)
        case "SPD":
            effected.adjust_spd_stage(amount)
        case "ACC":
            effected.adjust_acc_stage(amount)
        case "EVA":
            effected.adjust_eva_stage(amount)
        case "CRIT":
            effected.adjust_crit_stage(amount)
        case _:
            raise ValueError(f"Unable to parse stat change category {stat}, please provide a valid stat category.")


def apply_status_effect(effect_name: str, effected: Participant) -> None:
    status = NonVolatileStatusEnum[effect_name]
    effected.apply_status_non_volatile(status)
