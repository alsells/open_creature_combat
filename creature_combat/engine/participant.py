from creature_combat.creature.creature import creature
from creature_combat.moves.move import Move
from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
from creature_combat.utils.math_utils import clip

class Participant:
    def __init__(self):
        self.creature: creature = None
        self.reset_stage()
        
    def reset_stage(self) -> None:
        self._p_atk_stage:int = 0
        self._p_def_stage:int = 0
        self._s_atk_stage:int = 0
        self._s_def_stage:int = 0
        self._spd_stage:int = 0 
        self._acc_stage:int = 0
        self._eva_stage:int = 0
        self._crit_stage:int = 0

    def _adjust_hp(self, ammount: int) -> None:
        self.creature._current_hp = clip(self.creature.current_hp+ammount, 0, self.creature.max_hp)
    
    def heal(self, ammount: int) -> None:
        self._adjust_hp(ammount)
        
    def damage(self, ammount: int) -> None:
        self._adjust_hp(-ammount)
    
    def adjust_p_atk_stage(self, ammount: int) -> None:
        self._p_atk_stage = clip(self.p_atk_stage + ammount, -6, 6)
        
    def adjust_p_def_stage(self, ammount: int) -> None:
        self._p_def_stage = clip(self.p_def_stage + ammount, -6, 6)
        
    def adjust_s_atk_stage(self, ammount: int) -> None:
        self._s_atk_stage = clip(self.s_atk_stage + ammount, -6, 6)
        
    def adjust_s_def_stage(self, ammount: int) -> None:
        self._s_def_stage = clip(self.s_def_stage + ammount, -6, 6)
        
    def adjust_spd_stage(self, ammount: int) -> None:
        self._spd_stage = clip(self.spd_stage + ammount, -6, 6)
        
    def adjust_acc_stage(self, ammount: int) -> None:
        self._acc_stage = clip(self.acc_stage + ammount, -6, 6)
        
    def adjust_eva_stage(self, ammount: int) -> None:
        self._eva_stage = clip(self.eva_stage + ammount, -6, 6)
        
    def adjust_crit_stage(self, ammount: int) -> None:
        self._crit_stage = clip(self.crit_stage + ammount, 0, 6)
        
    def remove_creature(self) -> None:
        self.creature = None
        self.reset_stage()
        
    def add_creature(self, creature: creature) -> None:
        self.creature = creature
        
    def apply_status(self, status: NonVolatileStatusEnum) -> None:
        if self.creature.status.value == -1:
            self.creature._status = status

    def remove_status(self) -> None:
        self.creature._status = NonVolatileStatusEnum.NONE
        
    def can_make_move(self, move_name: str) -> bool:
        remaining_pp = self.creature._remaining_pp.get(move_name, None)
        return remaining_pp is not None and remaining_pp > 0
    
    def make_move(self, move_name: str) -> Move:
        self.creature._remaining_pp[move_name] -= 1
        move = [pm for pm in self.creature._moves if pm is not None and pm.name == move_name][0]
        return move
    
    @property
    def is_alive(self) -> bool:
        return self.creature if self.creature is None else self.creature.is_alive
    
    @property
    def lvl(self) -> int:
        return 0 if self.creature is None else self.creature.level
    
    @property
    def p_atk_stage(self) -> int:
        return 0 if self.creature is None else self._p_atk_stage 
    
    @property
    def p_atk(self) -> int:
        return 0 if self.creature is None else self.creature.p_atk
    
    @property
    def p_def_stage(self) -> int:
        return 0 if self.creature is None else self._p_def_stage
    
    @property
    def p_def(self) -> int:
        return 0 if self.creature is None else self.creature.p_def
    
    @property
    def s_atk_stage(self) -> int:
        return 0 if self.creature is None else self._s_atk_stage
    
    @property
    def s_atk(self) -> int:
        return 0 if self.creature is None else self.creature.s_atk
    
    @property
    def s_def_stage(self) -> int:
        return 0 if self.creature is None else self._s_def_stage
    
    @property
    def s_def(self) -> int:
        return 0 if self.creature is None else self.creature.s_def
    
    @property
    def spd_stage(self) -> int:
        return 0 if self.creature is None else self._spd_stage
    
    @property
    def spd(self) -> int:
        return 0 if self.creature is None else self.creature.spd
    
    @property
    def acc_stage(self) -> int:
        return 0 if self.creature is None else self._acc_stage
    
    @property
    def eva_stage(self) -> int:
        return 0 if self.creature is None else self._eva_stage
    
    @property
    def crit_stage(self) -> int:
        return 0 if self.creature is None else self._crit_stage
    