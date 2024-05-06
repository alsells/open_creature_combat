from numpy import array
from numpy.random import randint
from typing import Tuple, Optional

from creature_combat.creature.creature_base_stats import CreatureBaseStats
from creature_combat.creature.creature_natures import CreatureNatureEnum
from creature_combat.creature.effort_values import EffortValues
from creature_combat.creature.creature_types import CreatureTypeEnum
from creature_combat.creature.individual_values import IndividualValues
from creature_combat.moves.move import Move
from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
from creature_combat.utils.mappings import NATURE_MODIFIER
from creature_combat.utils.math_utils import clip


class Creature:
    def __init__(self, name: str, level: int, base_stats: CreatureBaseStats, individual_values: IndividualValues, effort_values: EffortValues, nature: CreatureNatureEnum, 
                 types: Tuple[CreatureTypeEnum, Optional[CreatureTypeEnum]], moves: Tuple[Move, Optional[Move], Optional[Move], Optional[Move]]):
        self.name:str = name
        self.level:int = level
        self._base_stats:CreatureBaseStats = base_stats
        self._individual_values:IndividualValues = individual_values
        self._effort_values:EffortValues = effort_values
        self._nature:CreatureNatureEnum = nature
        self._types:Tuple[CreatureTypeEnum, Optional[CreatureTypeEnum]] = types
        self._moves:Tuple[Move, Optional[Move], Optional[Move], Optional[Move]] = moves
        self._compute_stats()
        self._status: NonVolatileStatusEnum = NonVolatileStatusEnum.NONE
        self._status_duration: int = 0
        self._remaining_pp = {move.name: move.max_pp for move in self._moves if move is not None}
        self._move_map = {move.name: move for move in self._moves if move is not None}
    
    def _compute_hp(self) -> None:
        """Computes the creatures maximum health points based on the provided base stats, IV, EV, and level information. Equation is the GEN 3+ equation provided here: https://bulbapedia.bulbagarden.net/wiki/Stat
        """
        self._max_hp: int = int((2 * self._base_stats.health_points + self._individual_values.health_point + (self._effort_values.health_point / 4)) * (self.level / 100)) + self.level + 10
        self._current_hp: int = self._max_hp
    
    @staticmethod
    def _compute_stat(level: int, base: int, iv: int, ev: int) -> float:
        """Computes the Creature's stat value based on the base stat, IV, EV, and level of the creature. Equation is the GEN 3+ equation provided here: https://bulbapedia.bulbagarden.net/wiki/Stat

        Args:
            level (int): Level of the creature
            base (int): Base Stat Value for the stat being computed
            iv (int): Individual Value for the stat being computed 
            ev (int): Effort Value for the stat being computed

        Returns:
            float: Rough value of the Creature's stat before nature modification
        """
        stat = (2 * base + iv + (ev / 4)) * (level / 100) + 5
        return stat
    
    def _compute_stats(self) -> None:
        """Initialization method to determine and set all of the relevant stats for the Creature instance
        """
        self._compute_hp()
        p_atk = self._compute_stat(self.level, self._base_stats.physical_attack, self._individual_values.physical_attack, self._effort_values.physical_attack)
        p_def = self._compute_stat(self.level, self._base_stats.physical_defense, self._individual_values.physical_defense, self._effort_values.physical_defense)
        s_atk = self._compute_stat(self.level, self._base_stats.special_attack, self._individual_values.special_attack, self._effort_values.special_attack)
        s_def = self._compute_stat(self.level, self._base_stats.special_defense, self._individual_values.special_defense, self._effort_values.special_defense)
        spd = self._compute_stat(self.level, self._base_stats.speed, self._individual_values.speed, self._effort_values.speed)
        stat_arr = array([p_atk, p_def, s_atk, s_def, spd])
        # Modifier needs to be 1.0 by default, NATURE_MODIFIER only contains the deltas
        nature_mod = NATURE_MODIFIER[self._nature.value] + 1.0
        stats = stat_arr * nature_mod
        self._p_atk = int(stats[0])
        self._p_def = int(stats[1])
        self._s_atk = int(stats[2])
        self._s_def = int(stats[3])
        self._spd = int(stats[4])
        
    @property
    def is_alive(self) -> bool:
        """Helper attribute to determine if the Creature is alive or not, and thus available for combat.

        Returns:
            bool: Is the creature alive
        """
        return self._current_hp > 0
    
    def set_status(self, status: NonVolatileStatusEnum) -> None:
        """Sets the status of the Creature to the provided status value and the duration of that status effect. 

        Args:
            status (NonVolatileStatusEnum): What status is effecting the Creature.

        Raises:
            ValueError: If a non-valid status is provided, no duration information can be established so the program should crash.
        """
        if self._status.value == -1:    
            self._status = NonVolatileStatusEnum(status.value)
            match status:
                case NonVolatileStatusEnum.BRN:
                    duration = -1
                case NonVolatileStatusEnum.FRZ:
                    duration = -1
                case NonVolatileStatusEnum.PAR:
                    duration = -1
                case NonVolatileStatusEnum.PSN:
                    duration = -1
                case NonVolatileStatusEnum.BPSN:
                    duration = -1
                case NonVolatileStatusEnum.SLP:
                    duration = randint(1, 4)
                case NonVolatileStatusEnum.NONE:
                    duration = 0
                case _:
                    raise ValueError(f"Somehow NonVolatileStatusEnum had a non-expected value {status}")
            self._status_duration = duration
    
    def _reset_status(self) -> None:
        """Resets the Creature's status to NONE.
        """
        self._status = NonVolatileStatusEnum.NONE
        self._status_duration = 0
        
    def _reset_health(self) -> None:
        """Resets the Creature's current health back to its maximum health
        """
        self._current_hp = self._max_hp
        
    def _reset_pp(self) -> None:
        """Resets the PP value for all moves back to their maximum values
        """
        for move in self._moves:
            if move is not None:
                self._remaining_pp[move.name] = move.max_pp
    
    def reset_all(self) -> None:
        """Resets all relevant modifiable attributes of the Creature back to their starting/default values.
        """
        self._reset_status()
        self._reset_health()
        self._reset_pp()
        
    def adjust_health(self, amount: int) -> None:
        """Adjusts the health of the Creature by the provided amount. Will clip the lower bound to 0 and the upper bound to the max hp.

        Args:
            amount (int): How much should the current HP change.
        """
        self._current_hp = clip(self._current_hp + amount, 0, self._max_hp)
        
    def move_at_index(self, index: int) -> Optional[Move]:
        """Returns the move from the move list at the specified index. If none exists None will be returned instead.

        Args:
            index (int): What index of the move list should be returned.

        Returns:
            Optional[Move]: The move at that index or None.
        """
        if index < 4:
            return None if self._moves[index] is None else self._moves[index].name
        else:
            return None
        
    def index_of_move(self, move_name: str) -> Optional[int]:
        """Returns the index of the move based on the move_name provided.

        Args:
            move_name (str): The name of the move to find the index of

        Returns:
            Optional[int]: The index of the move in the move list for the provided name. If none is found None will be returned instead.
        """
        for idx, move in enumerate(self._moves):
            if move.name == move_name:
                return idx
        else:
            return None
        
    def is_stab(self, move: Move) -> bool:
        #TODO: Move the STAB check to combat functions and not as part of the Creature object
        """Determines if the move would gain the Same Type Attack Bonus (STAB) bonus when used by this creature.

        Args:
            move (Move): The move being questioned for STAB

        Returns:
            bool: True if the move would gain the bonus, False otherwise
        """
        return move.element in self._types
    
    @property
    def current_hp(self) -> int:
        """Accessor attribute for the creature's current HP 

        Returns:
            int: Creature's current HP
        """
        return self._current_hp
    
    @property
    def max_hp(self) -> int:
        """Accessor attribute for the creature's maximum HP 

        Returns:
            int: Creature's maximum HP
        """
        return self._max_hp
    
    @property
    def write_hp(self) -> str:
        """Generates a string to nicely display the health status of the Creature

        Returns:
            str: String for printout 
        """
        return f"[ {self.current_hp:03} / {self.max_hp:03} ]"

    @property
    def p_atk(self) -> int:
        """Accessor method for the Creature's Physical Attack

        Returns:
            int: Creature's Physical Attack
        """
        return self._p_atk
    
    @property
    def p_def(self) -> int:
        """Accessor method for the Creature's Physical Defense

        Returns:
            int: Creature's Physical Defense
        """
        return self._p_def
    
    @property
    def s_atk(self) -> int:
        """Accessor method for the Creature's Special Attack

        Returns:
            int: Creature's Special Attack
        """
        return self._s_atk
    
    @property
    def s_def(self) -> int:
        """Accessor method for the Creature's Special Defense

        Returns:
            int: Creature's Special Defense
        """
        return self._s_def
    
    @property
    def spd(self) -> int:
        """Accessor method for the Creature's Speed

        Returns:
            int: Creature's Speed
        """
        return self._spd
    
    @property
    def status(self) -> NonVolatileStatusEnum:
        """Accessor method for the Creature's Status Enum

        Returns:
            int: Creature's Status Enum
        """
        return self._status
    
    @property
    def status_duration(self) -> int:
        """Accessor method for the duration of the Creature's Status Enum

        Returns:
            int: Duration of the Creature's Status Enum

        """
        return self._status_duration
    
    @property
    def print_stats(self) -> str:
        """Generates a string to nicely print the stats of the Creature

        Returns:
            str: String to be printed
        """
        return f"====================\nHealth: {self.write_hp}\nPAtk: {self.p_atk}\nPDef: {self.p_def}\nSAtk: {self.s_atk}\nSDef: {self.s_def}\nSPD: {self.spd}\n===================="