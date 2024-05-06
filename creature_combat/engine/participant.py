from numpy.random import uniform
from creature_combat.creature.creature import Creature
from creature_combat.moves.move import Move
from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
from creature_combat.utils.math_utils import clip

class Participant:
    def __init__(self):
        self.creature: Creature = None
        self.reset_stage()
        self.bpsn_counter:int = 0
        
    def reset_stage(self) -> None:
        self._p_atk_stage:int = 0
        self._p_def_stage:int = 0
        self._s_atk_stage:int = 0
        self._s_def_stage:int = 0
        self._spd_stage:int = 0 
        self._acc_stage:int = 0
        self._eva_stage:int = 0
        self._crit_stage:int = 0

    def _adjust_hp(self, amount: int) -> None:
        self.creature._current_hp = clip(self.creature.current_hp+amount, 0, self.creature.max_hp)
    
    def heal(self, amount: int) -> None:
        self._adjust_hp(amount)
        
    def damage(self, amount: int) -> None:
        self._adjust_hp(-amount)
    
    def adjust_p_atk_stage(self, amount: int) -> None:
        self._p_atk_stage = clip(self.p_atk_stage + amount, -6, 6)
        
    def adjust_p_def_stage(self, amount: int) -> None:
        self._p_def_stage = clip(self.p_def_stage + amount, -6, 6)
        
    def adjust_s_atk_stage(self, amount: int) -> None:
        self._s_atk_stage = clip(self.s_atk_stage + amount, -6, 6)
        
    def adjust_s_def_stage(self, amount: int) -> None:
        self._s_def_stage = clip(self.s_def_stage + amount, -6, 6)
        
    def adjust_spd_stage(self, amount: int) -> None:
        self._spd_stage = clip(self.spd_stage + amount, -6, 6)
        
    def adjust_acc_stage(self, amount: int) -> None:
        self._acc_stage = clip(self.acc_stage + amount, -6, 6)
        
    def adjust_eva_stage(self, amount: int) -> None:
        self._eva_stage = clip(self.eva_stage + amount, -6, 6)
        
    def adjust_crit_stage(self, amount: int) -> None:
        self._crit_stage = clip(self.crit_stage + amount, 0, 6)
        
    def remove_creature(self) -> None:
        self.creature = None
        self.reset_stage()

    def add_creature(self, creature: Creature) -> None:
        self.creature = creature
        
    def apply_status_non_volatile(self, status: NonVolatileStatusEnum) -> None:
        self.creature.set_status(status)
        if status == NonVolatileStatusEnum.BPSN:
            self.bpsn_counter = 1

    def remove_status_non_volatile(self) -> None:
        self.creature._reset_status()
        
    def can_make_move(self, move_name: str) -> bool:
        remaining_pp = self.creature._remaining_pp.get(move_name, None)
        return remaining_pp is not None and remaining_pp > 0
    
    def make_move(self, move_name: str) -> Move:
        self.creature._remaining_pp[move_name] -= 1
        move = [pm for pm in self.creature._moves if pm is not None and pm.name == move_name][0]
        return move
    
    def apply_end_turn_effects(self):
        match self.creature.status:
            case NonVolatileStatusEnum.BRN:
                damage = int(self.creature.max_hp * 1/8)
                self.damage(damage)
            case NonVolatileStatusEnum.FRZ:
                thaws = uniform(0.0, 1.0) < 0.2
                if thaws:
                    self.remove_status_non_volatile()
            case NonVolatileStatusEnum.PSN:
                damage = int(self.creature.max_hp * 1/8)
                self.damage(damage)
            case NonVolatileStatusEnum.BPSN:
                damage = int(self.creature.max_hp * self.bpsn_counter / 16)
                self.damage(damage)
                self.bpsn_counter += 1
        if self.creature.status_duration != -1:
            self.creature._status_duration = max(self.creature.status_duration - 1, 0)
            if self.creature.status_duration == 0:
                self.remove_status_non_volatile()
    
    @property
    def is_alive(self) -> bool:
        return self.creature if self.creature is None else self.creature.is_alive
    
    @property
    def lvl(self) -> int:
        return 0 if self.creature is None else self.creature.level
    
    @property
    def current_hp(self) -> int:
        return 0 if self.creature is None else self.creature.current_hp
    
    @property
    def max_hp(self) -> int:
        return 0 if self.creature is None else self.creature.max_hp
    
    @property
    def p_atk_stage(self) -> int:
        return 0 if self.creature is None else self._p_atk_stage 
    
    @property
    def p_atk(self) -> int:
        if self.creature is None:
            return 0
        else:
            base = self.creature.p_atk
            stage = (2 + self.p_atk_stage) / 2 if self.p_atk_stage >= 0 else 2 / (2 - self.p_atk_stage)
            return int(base * stage)

    @property
    def p_def_stage(self) -> int:
        return 0 if self.creature is None else self._p_def_stage
    
    @property
    def p_def(self) -> int:
        if self.creature is None:
            return 0
        else:
            base = self.creature.p_def
            stage = (2 + self.p_def_stage) / 2 if self.p_def_stage >= 0 else 2 / (2 - self.p_def_stage)
            return int(base * stage)
    
    @property
    def s_atk_stage(self) -> int:
        return 0 if self.creature is None else self._s_atk_stage
    
    @property
    def s_atk(self) -> int:
        if self.creature is None:
            return 0
        else:
            base = self.creature.s_atk
            stage = (2 + self.s_atk_stage) / 2 if self.s_atk_stage >= 0 else 2 / (2 - self.s_atk_stage)
            return int(base * stage)
    
    @property
    def s_def_stage(self) -> int:
        return 0 if self.creature is None else self._s_def_stage
    
    @property
    def s_def(self) -> int:
        if self.creature is None:
            return 0
        else:
            base = self.creature.s_def
            stage = (2 + self.s_def_stage) / 2 if self.s_def_stage >= 0 else 2 / (2 - self.s_def_stage)
            return int(base * stage)
    
    @property
    def spd_stage(self) -> int:
        return 0 if self.creature is None else self._spd_stage
    
    @property
    def spd(self) -> int:
        if self.creature is None:
            return 0
        else:
            base = self.creature.spd
            stage = (2 + self.spd_stage) / 2 if self.spd_stage >= 0 else 2 / (2 - self.spd_stage)
            par_penalty = 0.5 if self.creature.status == NonVolatileStatusEnum.PAR else 1.0
            return int(base * stage * par_penalty)
    
    @property
    def acc_stage(self) -> int:
        return 0 if self.creature is None else self._acc_stage
    
    @property
    def eva_stage(self) -> int:
        return 0 if self.creature is None else self._eva_stage
    
    @property
    def crit_stage(self) -> int:
        return 0 if self.creature is None else self._crit_stage
    