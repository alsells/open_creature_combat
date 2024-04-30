from numpy import array
from typing import Tuple, Optional

from pokemon_combat.pokemon.pokemon_base_stats import PokemonBaseStats
from pokemon_combat.pokemon.pokemon_natures import PokemonNatureEnum
from pokemon_combat.pokemon.effort_values import EffortValues
from pokemon_combat.pokemon.pokemon_types import PokemonTypeEnum
from pokemon_combat.pokemon.individual_values import IndividualValues
from pokemon_combat.moves.move import Move
from pokemon_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
from pokemon_combat.utils.mappings import NATURE_MODIFIER
from pokemon_combat.utils.math_utils import clip


class Pokemon:
    def __init__(self, name: str, level: int, base_stats: PokemonBaseStats, individual_values: IndividualValues, effort_values: EffortValues, nature: PokemonNatureEnum, 
                 types: Tuple[PokemonTypeEnum, Optional[PokemonTypeEnum]], moves: Tuple[Move, Optional[Move], Optional[Move], Optional[Move]]):
        self.name:str = name
        self.level:int = level
        self._base_stats:PokemonBaseStats = base_stats
        self._individual_values:IndividualValues = individual_values
        self._effort_values:EffortValues = effort_values
        self._nature:PokemonNatureEnum = nature
        self._types:Tuple[PokemonTypeEnum, Optional[PokemonTypeEnum]] = types
        self._moves:Tuple[Move, Optional[Move], Optional[Move], Optional[Move]] = moves
        self._compute_stats()
        self._status: NonVolatileStatusEnum = NonVolatileStatusEnum.NONE
        self._remaining_pp = {move.name: move.max_pp for move in self._moves if move is not None}
        self._move_map = {move.name: move for move in self._moves if move is not None}
    
    def _compute_hp(self) -> None:
        self._max_hp: int = int((2 * self._base_stats.health_points + self._individual_values.health_point + (self._effort_values.health_point / 4)) * (self.level / 100)) + self.level + 10
        self._current_hp: int = self._max_hp
    
    @staticmethod
    def _compute_stat(level: int, base: int, iv: int, ev: int) -> float:
        stat = (2 * base + iv + (ev / 4)) * (level / 100) + 5
        return stat
    
    def _compute_stats(self) -> None:
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
    def is_alive(self):
        return self._current_hp > 0
    
    def set_status(self, status: NonVolatileStatusEnum) -> None:
        if self._status.value == -1:    
            self._status = NonVolatileStatusEnum(status.value)
    
    def _reset_status(self) -> None:
        self._status = NonVolatileStatusEnum.NONE
        
    def _reset_health(self) -> None:
        self._current_hp = self._max_hp
        
    def _reset_pp(self) -> None:
        for move in self._moves:
            if move is not None:
                self._remaining_pp[move.name] = move.max_pp
    
    def reset_all(self) -> None:
        self._reset_status()
        self._reset_health()
        self._reset_pp()
        
    def adjust_health(self, ammount: int) -> None:
        self._current_hp = clip(self._current_hp + ammount, 0, self._max_hp)
        
    def move_at_index(self, index: int) -> Optional[str]:
        if index < 4:
            return None if self._moves[index] is None else self._moves[index].name
        else:
            return None
        
    def index_of_move(self, move_name: str) -> Optional[int]:
        for idx, move in enumerate(self._moves):
            if move.name == move_name:
                return idx
        else:
            return None
        
    def is_stab(self, move: Move) -> bool:
        return move.element in self._types
    
    @property
    def current_hp(self) -> int:
        return self._current_hp
    
    @property
    def max_hp(self) -> int:
        return self._max_hp
    
    @property
    def write_hp(self) -> str:
        return f"[ {self.current_hp:03} / {self.max_hp:03} ]"

    @property
    def p_atk(self) -> int:
        return self._p_atk
    
    @property
    def p_def(self) -> int:
        return self._p_def
    
    @property
    def s_atk(self) -> int:
        return self._s_atk
    
    @property
    def s_def(self) -> int:
        return self._s_def
    
    @property
    def spd(self) -> int:
        return self._spd
    
    @property
    def status(self) -> NonVolatileStatusEnum:
        return self._status
    
    @property
    def print_stats(self) -> str:
        return f"====================\nHealth: {self.write_hp}\nPAtk: {self.p_atk}\nPDef: {self.p_def}\nSAtk: {self.s_atk}\nSDef: {self.s_def}\nSPD: {self.spd}\n===================="