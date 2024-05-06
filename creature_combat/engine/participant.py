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
        """Resets the stage for all of the stats back to the default of 0
        """
        self._p_atk_stage:int = 0
        self._p_def_stage:int = 0
        self._s_atk_stage:int = 0
        self._s_def_stage:int = 0
        self._spd_stage:int = 0 
        self._acc_stage:int = 0
        self._eva_stage:int = 0
        self._crit_stage:int = 0

    def _adjust_hp(self, amount: int) -> None:
        """Adjusts the current HP of the owned Creature by the provided amount.

        Args:
            amount (int): How much to change the current health by
        """
        self.creature._current_hp = clip(self.creature.current_hp+amount, 0, self.creature.max_hp)
    
    def heal(self, amount: int) -> None:
        """Applies a positive HP adjustment to the creature.

        Args:
            amount (int): How much to heal the creature by
        """
        self._adjust_hp(abs(amount))
        
    def damage(self, amount: int) -> None:
        """Applies a negative HP adjustment to the creature.

        Args:
            amount (int): How much to damage the creature by
        """
        self._adjust_hp(-abs(amount))
    
    def adjust_p_atk_stage(self, amount: int) -> None:
        """Adjusts the p-atk stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the p-atk stage by 
        """
        self._p_atk_stage = clip(self.p_atk_stage + amount, -6, 6)
        
    def adjust_p_def_stage(self, amount: int) -> None:
        """Adjusts the p-def stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the p-def stage by 
        """
        self._p_def_stage = clip(self.p_def_stage + amount, -6, 6)
        
    def adjust_s_atk_stage(self, amount: int) -> None:
        """Adjusts the s-atk stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the s-atk stage by 
        """
        self._s_atk_stage = clip(self.s_atk_stage + amount, -6, 6)
        
    def adjust_s_def_stage(self, amount: int) -> None:
        """Adjusts the s-def stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the s-def stage by 
        """
        self._s_def_stage = clip(self.s_def_stage + amount, -6, 6)
        
    def adjust_spd_stage(self, amount: int) -> None:
        """Adjusts the speed stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the speed stage by 
        """
        self._spd_stage = clip(self.spd_stage + amount, -6, 6)
        
    def adjust_acc_stage(self, amount: int) -> None:
        """Adjusts the accuracy stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the accuracy stage by 
        """
        self._acc_stage = clip(self.acc_stage + amount, -6, 6)
        
    def adjust_eva_stage(self, amount: int) -> None:
        """Adjusts the evasion stage by the amount provided, clipping to keep the value on the range of [-6, 6]

        Args:
            amount (int): How much to change the evasion stage by 
        """
        self._eva_stage = clip(self.eva_stage + amount, -6, 6)
        
    def adjust_crit_stage(self, amount: int) -> None:
        """Adjusts the critical stage by the amount provided, clipping to keep the value on the range of [-0, 6]

        Args:
            amount (int): How much to change the critical stage by 
        """
        self._crit_stage = clip(self.crit_stage + amount, 0, 6)
        
    def remove_creature(self) -> None:
        """Removes the creature from the participant in the battle. Resets all stat stage changes to the creature.
        """
        self.creature = None
        self.reset_stage()

    def add_creature(self, creature: Creature) -> None:
        """Adds a creature to the participant in the battle.

        Args:
            creature (Creature): The creature now in battle.
        """
        self.creature = creature
        
    def apply_status_non_volatile(self, status: NonVolatileStatusEnum) -> None:
        """Applies the non-volatile status to the owned Creature.

        Args:
            status (NonVolatileStatusEnum): The status afflicting the Creature
        """
        self.creature.set_status(status)
        if status == NonVolatileStatusEnum.BPSN:
            self.bpsn_counter = 1

    def remove_status_non_volatile(self) -> None:
        """Removes the non-volatile status from the owned Creature
        """
        self.creature._reset_status()
        
    def can_make_move(self, move_name: str) -> bool:
        """Checks if the move_name move still has pp uses remaining. If so the move is useable.

        Args:
            move_name (str): Name of the move to determine usability for

        Returns:
            bool: Can the move be used or not 
        """
        remaining_pp = self.creature._remaining_pp.get(move_name, None)
        return remaining_pp is not None and remaining_pp > 0
    
    def make_move(self, move_name: str) -> Move:
        """Makes the move provided by the move_name for the round in combat. Will also decrement 1 PP usage. 

        Args:
            move_name (str): Name of the move to use

        Returns:
            Move: Move used by the participant this round 
        """
        self.creature._remaining_pp[move_name] -= 1
        move = [pm for pm in self.creature._moves if pm is not None and pm.name == move_name][0]
        return move
    
    def apply_end_turn_effects(self):
        #TODO: Include other effects that trigger at round end to this method
        """Applies the end turn effect of the Creatures status. 
        """
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
    
    @staticmethod
    def _stat_stage_modifier(stage: int) -> float:
        """How much does the current stat stage effect the base stat of the creature. Follows the equation for GEN2+: max(2, 2+stage)/max(2,2-stage) 
        as described here: https://www.dragonflycave.com/mechanics/stat-stages

        Args:
            stage (int): Stage level

        Returns:
            float: Modifier for the base stat of the creature
        """
        return (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)
    
    @property
    def is_alive(self) -> bool:
        """Wrapper accessor method of the Creature's is_alive attribute

        Returns:
            bool: Is the active creature alive or not 
        """
        return False if self.creature is None else self.creature.is_alive
    
    @property
    def lvl(self) -> int:
        """Wrapper accessor method of the Creature's level attribute 

        Returns:
            int: Level of the active creature
        """
        return 0 if self.creature is None else self.creature.level
    
    @property
    def current_hp(self) -> int:
        """Wrapper accessor method of the Creature's current_hp attribute 

        Returns:
            int: Current HP of the active creature
        """
        return 0 if self.creature is None else self.creature.current_hp
    
    @property
    def max_hp(self) -> int:
        """Wrapper accessor method of the Creature's max_hp attribute 

        Returns:
            int: Maximum HP of the active creature
        """
        return 0 if self.creature is None else self.creature.max_hp
    
    @property
    def p_atk_stage(self) -> int:
        """Accessor method for the physical attack stage of the current participant 

        Returns:
            int: Current physical attack stage of the participant
        """
        return 0 if self.creature is None else self._p_atk_stage 
    
    @property
    def p_atk(self) -> int:
        """Effective physical attack for the participant, adjusted by the current physical attack stage

        Returns:
            int: Effective physical attack of the creature
        """
        return 0 if self.creature is None else int(self.creature.p_atk * self._stat_stage_modifier(self.p_atk_stage))

    @property
    def p_def_stage(self) -> int:
        """Accessor method for the physical defense stage of the current participant 

        Returns:
            int: Current physical defense stage of the participant
        """
        return 0 if self.creature is None else self._p_def_stage
    
    @property
    def p_def(self) -> int:
        """Effective physical defense for the participant, adjusted by the current physical defense stage

        Returns:
            int: Effective physical defense of the creature
        """
        return 0 if self.creature is None else int(self.creature.p_def * self._stat_stage_modifier(self.p_def_stage))
    
    @property
    def s_atk_stage(self) -> int:
        """Accessor method for the special attack stage of the current participant 

        Returns:
            int: Current special attack stage of the participant
        """
        return 0 if self.creature is None else self._s_atk_stage
    
    @property
    def s_atk(self) -> int:
        """Effective special attack for the participant, adjusted by the current special attack stage

        Returns:
            int: Effective special attack of the creature
        """
        return 0 if self.creature is None else int(self.creature.s_atk * self._stat_stage_modifier(self.s_atk_stage))
    
    @property
    def s_def_stage(self) -> int:
        """Accessor method for the special defense stage of the current participant 

        Returns:
            int: Current special defense stage of the participant
        """
        return 0 if self.creature is None else self._s_def_stage
    
    @property
    def s_def(self) -> int:
        """Effective special defense for the participant, adjusted by the current special defense stage

        Returns:
            int: Effective special defense of the creature
        """
        return 0 if self.creature is None else int(self.creature.s_def * self._stat_stage_modifier(self.s_def_stage))
    
    @property
    def spd_stage(self) -> int:
        """Accessor method for the speed stage of the current participant 

        Returns:
            int: Current speed stage of the participant
        """
        return 0 if self.creature is None else self._spd_stage
    
    @property
    def spd(self) -> int:
        """Effective speed for the participant, adjusted by the current speed stage

        Returns:
            int: Effective physical defense of the creature
        """
        return 0 if self.creature is None else int(self.creature.spd * self._stat_stage_modifier(self.spd_stage))
    
    @property
    def acc_stage(self) -> int:
        """Accessor method for the accuracy stage of the current participant 

        Returns:
            int: Current accuracy stage of the participant
        """
        return 0 if self.creature is None else self._acc_stage
    
    @property
    def eva_stage(self) -> int:
        """Accessor method for the evasion stage of the current participant 

        Returns:
            int: Current evasion stage of the participant
        """
        return 0 if self.creature is None else self._eva_stage
    
    @property
    def crit_stage(self) -> int:
        """Accessor method for the critical stage of the current participant 

        Returns:
            int: Current critical stage of the participant
        """
        return 0 if self.creature is None else self._crit_stage
    