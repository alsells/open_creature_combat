from typing import List
from numpy.random import uniform
from creature_combat.engine.player import Player
from creature_combat.engine.participant import Participant
from creature_combat.engine.combat_functions import calculate_damage, participant_1_first, adjust_stat_stage, does_hit, apply_status_effect
from creature_combat.moves.move import Move
from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum


class CombatManager:
    def __init__(self, display_messages: bool=False):
        # TODO: Figure out how to handle the environment
        self.environment = None
        self.round_number = 0
        self.message_queue: List[str] = [""]
        self.display_messages = display_messages
    
    def reset(self, player_1: Player, player_2: Player):
        player_1.swap_creature(None)
        player_2.swap_creature(None)
        self.round_number = 0
        self.environment = None
        self.message_queue = [""]
        
    def _queue_message(self, message: str):
        if self.display_messages:
            self.message_queue.append(message)
            
    def _apply_effects(self, effect: str, effected: Participant):
        if ":" in effect:
            effect_type, amount = effect.split(':')
            amount = int(amount)
            if "HEAL" in effect_type:
                if "%" in effect_type:
                    effected.heal(effected.creature.max_hp * amount / 100)
                elif "FLAT" in effect_type:
                    effected.heal(amount)
                else:
                    raise ValueError(f"Can not parse heal effect type {effect_type}")
            else:
                adjust_stat_stage(effect_type, effected)
        else:
            apply_status_effect(effect, effected)
    
    def _apply_action(self, attacker_move: Move, attacker: Participant, defender: Participant):
        can_move = uniform(0.0, 1.0) < 0.25 if attacker.creature.status == NonVolatileStatusEnum.PAR else True
        if can_move:
            if attacker_move.is_attack:
                if does_hit(attacker_move, attacker, defender):
                    damage = calculate_damage(attacker_move, attacker, defender)
                    self._queue_message(f"{attacker.creature.name} dealt {damage} to {defender.creature.name}!")
                    defender.damage(damage)
                    lifesteal = [se for se in attacker_move.self_effect if "LIFESTEAL" in se]
                    if len(lifesteal) > 0:
                        lifesteal = lifesteal[0]
                        heal_type, amount = lifesteal.split(':')
                        amount = int(amount)
                        if "%" in heal_type:
                            attacker.heal(damage * amount/100)
                        elif "FLAT" in heal_type:
                            attacker.heal(amount)
                        else:
                            raise ValueError(f"Can not parse life-steal effect type {heal_type}")
                else:
                    self._queue_message(f"{attacker.creature.name}'s attacked missed!")
            for self_effect in attacker_move.self_effect:
                self._apply_effects(self_effect, attacker)
            for opponent_effect in attacker_move.opponent_effect:
                self._apply_effects(opponent_effect, defender)
            # TODO: Add environmental factors to moves
            for env_effect in attacker_move.environment_effect:
                pass
        else:
            self._queue_message(f"{attacker.creature.name} was paralyzed and could not move.")
        
    def _apply_end_turn_effects(self, attacker: Participant, defender: Participant):
        attacker.apply_end_turn_effects()
        defender.apply_end_turn_effects()
    
    def take_turn(self, player_1: Player, player_2: Player):
        self.round_number += 1
        player_1_move = player_1.make_move(player_2.participant)
        player_2_move = player_2.make_move(player_1.participant)
        player_1_first = participant_1_first(player_1.participant, player_1_move, player_2.participant, player_2_move)
        if player_1_first:
            self._apply_action(player_1_move, player_1.participant, player_2.participant)
            if player_2.participant.is_alive:
                self._apply_action(player_2_move, player_2.participant, player_1.participant)
            self._queue_message(f"{player_1.participant.creature.name} HP: {player_1.participant.creature.write_hp}")
            self._queue_message(f"{player_2.participant.creature.name} HP: {player_2.participant.creature.write_hp}")
        else:
            self._apply_action(player_2_move, player_2.participant, player_1.participant)
            if player_1.participant.is_alive:
                self._apply_action(player_1_move, player_1.participant, player_2.participant)
            self._queue_message(f"{player_2.participant.creature.name} HP: {player_2.participant.creature.write_hp}")
            self._queue_message(f"{player_1.participant.creature.name} HP: {player_1.participant.creature.write_hp}")
        if not player_1.participant.is_alive:
            self._queue_message(f"{player_1.participant.creature.name} has fainted!")
            player_1.swap_creature(player_2.participant)
        if not player_2.participant.is_alive:
            self._queue_message(f"{player_2.participant.creature.name} has fainted!")
            player_2.swap_creature(player_1.participant)
        self._queue_message(f"Round: {self.round_number:02d} completed!")
        if self.display_messages:
            self._queue_message("")
            for message in self.message_queue:
                print(message)
        self.message_queue.clear()
        self._queue_message("")
