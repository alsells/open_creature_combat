import unittest

from creature_combat.engine.participant import Participant
from creature_combat.creature.creaturedex import CreatureEntry
from creature_combat.creature.creature_natures import CreatureNatureEnum
from creature_combat.creature.effort_values import EffortValues
from creature_combat.creature.individual_values import IndividualValues
from creature_combat.moves.move import Move
from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
from creature_combat.utils.path_utils import _CREATUREDEX_PATH, _MOVE_LIST_PATH


class TestParticipant(unittest.TestCase):
    def setUp(self) -> None:
        creature_entry = CreatureEntry.from_json(_CREATUREDEX_PATH / "Bulbasaur.json")
        moves = (Move.from_json(_MOVE_LIST_PATH / "Tackle.json"), Move.from_json(_MOVE_LIST_PATH / "Growl.json"), Move.from_json(_MOVE_LIST_PATH / "Vine Whip.json"),None)
        evs = EffortValues.make_zero()
        ivs = IndividualValues.make_zero()
        nature = CreatureNatureEnum.BASHFUL
        self.creature = creature_entry.make_creature(5, ivs, evs, nature, moves)
        self.participant = Participant()
        self.participant.add_creature(self.creature)
        
    def test_adjust_p_atk_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_p_atk_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.p_atk_stage, -6, "P-atk stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.p_atk_stage, 6, "P-atk stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.p_atk_stage, n, "P-atk stage did not set properly.")
            self.participant._p_atk_stage = 0
            
    def test_adjust_p_def_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_p_def_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.p_def_stage, -6, "P-def stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.p_def_stage, 6, "P-def stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.p_def_stage, n, "P-def stage did not set properly.")
            self.participant._p_def_stage = 0
            
    def test_adjust_s_atk_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_s_atk_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.s_atk_stage, -6, "S-atk stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.s_atk_stage, 6, "S-atk stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.s_atk_stage, n, "S-atk stage did not set properly.")
            self.participant._s_atk_stage = 0
            
    def test_adjust_s_def_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_s_def_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.s_def_stage, -6, "S-def stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.s_def_stage, 6, "S-def stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.s_def_stage, n, "S-def stage did not set properly.")
            self.participant._s_def_stage = 0
            
    def test_adjust_spd_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_spd_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.spd_stage, -6, "Speed stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.spd_stage, 6, "Speed stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.spd_stage, n, "Speed stage did not set properly.")
            self.participant._spd_stage = 0
            
    def test_adjust_acc_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_acc_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.acc_stage, -6, "Accuracy stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.acc_stage, 6, "Accuracy stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.acc_stage, n, "Accuracy stage did not set properly.")
            self.participant._acc_stage = 0
            
    def test_adjust_eva_stage(self):
        for n in range(-7, 8):
            with self.subTest(n=n):
                self.participant.adjust_eva_stage(n)
                if n < -6:
                    self.assertEqual(self.participant.eva_stage, -6, "Evasion stage did not clip values below the range [-6, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.eva_stage, 6, "Evasion stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.eva_stage, n, "Evasion stage did not set properly.")
            self.participant._eva_stage = 0
            
    def test_adjust_crit_stage(self):
        for n in range(-1, 8):
            with self.subTest(n=n):
                self.participant.adjust_crit_stage(n)
                if n < 0:
                    self.assertEqual(self.participant.crit_stage, 0, "Critical stage did not clip values below the range [0, 6]")
                elif n > 6:
                    self.assertEqual(self.participant.crit_stage, 6, "Critical stage did not clip values above the range [-6, 6]")
                else:
                    self.assertEqual(self.participant.crit_stage, n, "Critical stage did not set properly.")
            self.participant._crit_stage = 0
    
    def test_reset_stage(self):
        self.participant.adjust_p_atk_stage(1)
        self.participant.adjust_p_def_stage(2)
        self.participant.adjust_s_atk_stage(3)
        self.participant.adjust_s_def_stage(-1)
        self.participant.adjust_spd_stage(-2)
        self.participant.adjust_crit_stage(-3)
        self.participant.adjust_eva_stage(3)
        self.participant.adjust_acc_stage(1)
        self.participant.reset_stage()
        self.assertEqual(self.participant.p_atk_stage, 0, "P-atk stage was not reset.")
        self.assertEqual(self.participant.p_def_stage, 0, "P-def stage was not reset.")
        self.assertEqual(self.participant.s_atk_stage, 0, "S-atk stage was not reset.")
        self.assertEqual(self.participant.s_def_stage, 0, "S-def stage was not reset.")
        self.assertEqual(self.participant.spd_stage, 0, "Speed stage was not reset.")
        self.assertEqual(self.participant.acc_stage, 0, "Accuracy stage was not reset.")
        self.assertEqual(self.participant.eva_stage, 0, "Evasion stage was not reset.")
        self.assertEqual(self.participant.crit_stage, 0, "Critical stage was not reset.")
        
    def test_effective_p_atk(self):
        for n in range(-6, 6):
            with self.subTest(n=n):
                self.participant.adjust_p_atk_stage(n)
                match self.participant.p_atk_stage:
                    case -6:
                        mod = 2/8
                    case -5:
                        mod = 2/7
                    case -4:
                        mod = 2/6
                    case -3:
                        mod = 2/5
                    case -2:
                        mod = 2/4
                    case -1:
                        mod = 2/3
                    case 0:
                        mod = 2/2
                    case 1:
                        mod = 3/2
                    case 2:
                        mod = 4/2
                    case 3:
                        mod = 5/2
                    case 4:
                        mod = 6/2
                    case 5:
                        mod = 7/2
                    case 6:
                        mod = 8/2
                    case _:
                        raise ValueError("Stage modifier not defined outside of [-6, 6]")
                truth = int(self.creature.p_atk * mod)
                self.assertEqual(self.participant.p_atk, truth, "Participant p-atk did not match expected")
                self.participant.reset_stage()
                
    def test_effective_p_def(self):
        for n in range(-6, 6):
            with self.subTest(n=n):
                self.participant.adjust_p_def_stage(n)
                match self.participant.p_def_stage:
                    case -6:
                        mod = 2/8
                    case -5:
                        mod = 2/7
                    case -4:
                        mod = 2/6
                    case -3:
                        mod = 2/5
                    case -2:
                        mod = 2/4
                    case -1:
                        mod = 2/3
                    case 0:
                        mod = 2/2
                    case 1:
                        mod = 3/2
                    case 2:
                        mod = 4/2
                    case 3:
                        mod = 5/2
                    case 4:
                        mod = 6/2
                    case 5:
                        mod = 7/2
                    case 6:
                        mod = 8/2
                    case _:
                        raise ValueError("Stage modifier not defined outside of [-6, 6]")
                truth = int(self.creature.p_atk * mod)
                self.assertEqual(self.participant.p_def, truth, "Participant p-def did not match expected")
                self.participant.reset_stage()
                
    def test_effective_p_def(self):
        for n in range(-6, 6):
            with self.subTest(n=n):
                self.participant.adjust_p_def_stage(n)
                match self.participant.p_def_stage:
                    case -6:
                        mod = 2/8
                    case -5:
                        mod = 2/7
                    case -4:
                        mod = 2/6
                    case -3:
                        mod = 2/5
                    case -2:
                        mod = 2/4
                    case -1:
                        mod = 2/3
                    case 0:
                        mod = 2/2
                    case 1:
                        mod = 3/2
                    case 2:
                        mod = 4/2
                    case 3:
                        mod = 5/2
                    case 4:
                        mod = 6/2
                    case 5:
                        mod = 7/2
                    case 6:
                        mod = 8/2
                    case _:
                        raise ValueError("Stage modifier not defined outside of [-6, 6]")
                truth = int(self.creature.p_def * mod)
                self.assertEqual(self.participant.p_def, truth, "Participant p-def did not match expected")
                self.participant.reset_stage()
                
    def test_effective_s_atk(self):
        for n in range(-6, 6):
            with self.subTest(n=n):
                self.participant.adjust_s_atk_stage(n)
                match self.participant.s_atk_stage:
                    case -6:
                        mod = 2/8
                    case -5:
                        mod = 2/7
                    case -4:
                        mod = 2/6
                    case -3:
                        mod = 2/5
                    case -2:
                        mod = 2/4
                    case -1:
                        mod = 2/3
                    case 0:
                        mod = 2/2
                    case 1:
                        mod = 3/2
                    case 2:
                        mod = 4/2
                    case 3:
                        mod = 5/2
                    case 4:
                        mod = 6/2
                    case 5:
                        mod = 7/2
                    case 6:
                        mod = 8/2
                    case _:
                        raise ValueError("Stage modifier not defined outside of [-6, 6]")
                truth = int(self.creature.s_atk * mod)
                self.assertEqual(self.participant.s_atk, truth, "Participant s-atk did not match expected")
                self.participant.reset_stage()
                
    def test_effective_p_def(self):
        for n in range(-6, 6):
            with self.subTest(n=n):
                self.participant.adjust_s_def_stage(n)
                match self.participant.s_def_stage:
                    case -6:
                        mod = 2/8
                    case -5:
                        mod = 2/7
                    case -4:
                        mod = 2/6
                    case -3:
                        mod = 2/5
                    case -2:
                        mod = 2/4
                    case -1:
                        mod = 2/3
                    case 0:
                        mod = 2/2
                    case 1:
                        mod = 3/2
                    case 2:
                        mod = 4/2
                    case 3:
                        mod = 5/2
                    case 4:
                        mod = 6/2
                    case 5:
                        mod = 7/2
                    case 6:
                        mod = 8/2
                    case _:
                        raise ValueError("Stage modifier not defined outside of [-6, 6]")
                truth = int(self.creature.s_def * mod)
                self.assertEqual(self.participant.s_def, truth, "Participant s-def did not match expected")
                self.participant.reset_stage()
                
    def test_effective_p_def(self):
        for n in range(-6, 6):
            with self.subTest(n=n):
                self.participant.adjust_spd_stage(n)
                match self.participant.spd_stage:
                    case -6:
                        mod = 2/8
                    case -5:
                        mod = 2/7
                    case -4:
                        mod = 2/6
                    case -3:
                        mod = 2/5
                    case -2:
                        mod = 2/4
                    case -1:
                        mod = 2/3
                    case 0:
                        mod = 2/2
                    case 1:
                        mod = 3/2
                    case 2:
                        mod = 4/2
                    case 3:
                        mod = 5/2
                    case 4:
                        mod = 6/2
                    case 5:
                        mod = 7/2
                    case 6:
                        mod = 8/2
                    case _:
                        raise ValueError("Stage modifier not defined outside of [-6, 6]")
                truth = int(self.creature.spd * mod)
                self.assertEqual(self.participant.spd, truth, "Participant speed did not match expected")
                self.participant.reset_stage()
                
    def test_healing(self):
        self.participant.creature._reset_health()
        self.participant.creature._current_hp = 0
        self.participant.heal(5)
        self.assertEqual(self.participant.creature.current_hp, 5, "Creature did not properly heal from participant's heal function")
        
    def test_damage(self):
        self.participant.creature._reset_health()
        self.participant.damage(5)
        self.assertEqual(self.participant.current_hp, self.participant.max_hp - 5, "Creature did not properly take damage from participant's damage function")
        
    def test_end_turn_effects(self):
        for n, status in enumerate(NonVolatileStatusEnum):
            with self.subTest(n=n):
                self.participant.creature._reset_health()
                self.participant.remove_status_non_volatile()
                self.participant.apply_status_non_volatile(status)
                self.participant.apply_end_turn_effects()
                match status:
                    case NonVolatileStatusEnum.BRN:
                        self.assertEqual(self.participant.current_hp, self.participant.max_hp - int(self.participant.max_hp * 1/8), "Burn status did not properly apply damage")
                    case NonVolatileStatusEnum.PSN:
                        self.assertEqual(self.participant.current_hp, self.participant.max_hp - int(self.participant.max_hp * 1/8), "Poison status did not properly apply damage")
                    case NonVolatileStatusEnum.BPSN:
                        self.assertEqual(self.participant.current_hp, self.participant.max_hp - int(self.participant.max_hp * 1/16), "Poison status did not properly apply damage")
        
        
if __name__ == "__main__":
    unittest.main()