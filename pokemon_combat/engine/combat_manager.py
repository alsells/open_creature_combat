from typing import List

from pokemon_combat.engine.player import Player
from pokemon_combat.engine.participant import Participant
from pokemon_combat.engine.combat_functions import calculate_damge, plarticipant_1_first, apply_status, does_hit
from pokemon_combat.moves.move import Move
from pokemon_combat.moves.move_types import MoveTypeEnum


class CombatManager:
    def __init__(self, display_messsages: bool=False):
        # TODO: Figure out how to handle the environment
        self.environment = None
        self.round_number = 0
        self.message_queue: List[str] = [""]
        self.display_messages = display_messsages
    
    def reset(self, player_1: Player, player_2: Player):
        player_1.swap_pokemon(None)
        player_2.swap_pokemon(None)
        self.round_number = 0
        self.environment = None
        self.message_queue = [""]
        
    def _apply_status(self, attacker_move: Move, attacker: Participant, defender: Participant):
        for self_effect in attacker_move.self_effect:
            if len(self_effect.name.split('_')) == 3:
                apply_status(attacker_move.name, attacker, defender, True)
            
        for opp_effect in attacker_move.opponent_effect:
            if len(opp_effect.name.split('_')) == 3:
                apply_status(attacker_move.name, attacker, defender, False)
        for env_effect in attacker_move.environment_effect:
            # TODO: Figure out how environmental effects are handled here
            continue

    def _apply_action(self, attacker_move: Move, attacker: Participant, defender: Participant):
        if attacker_move.move_type == MoveTypeEnum.STATUS:
            self._apply_status(attacker_move, attacker, defender)
        else:
            if does_hit(attacker_move, attacker, defender):
                defender_damage = calculate_damge(attacker_move, attacker, defender)
                self.message_queue.append(f"{attacker.pokemon.name} dealt {defender_damage:03d} damage to {defender.pokemon.name}")
                defender.damage(defender_damage)
            else:
                self.message_queue.append(f"{attacker.pokemon.name}'s attack missed!")
    
    def take_turn(self, player_1: Player, player_2: Player):
        self.round_number += 1
        player_1_move = player_1.make_move(player_2.participant)
        player_2_move = player_2.make_move(player_1.participant)
        player_1_first = plarticipant_1_first(player_1.participant, player_1_move, player_2.participant, player_2_move)
        if player_1_first:
            self._apply_action(player_1_move, player_1.participant, player_2.participant)
            if player_2.participant.is_alive:
                self._apply_action(player_2_move, player_2.participant, player_1.participant)
            self.message_queue.append(f"{player_1.participant.pokemon.name} HP: {player_1.participant.pokemon.write_hp}")
            self.message_queue.append(f"{player_2.participant.pokemon.name} HP: {player_2.participant.pokemon.write_hp}")
        else:
            self._apply_action(player_2_move, player_2.participant, player_1.participant)
            if player_1.participant.is_alive:
                self._apply_action(player_1_move, player_1.participant, player_2.participant)
            self.message_queue.append(f"{player_2.participant.pokemon.name} HP: {player_2.participant.pokemon.write_hp}")
            self.message_queue.append(f"{player_1.participant.pokemon.name} HP: {player_1.participant.pokemon.write_hp}")
        if not player_1.participant.is_alive:
            self.message_queue.append(f"{player_1.participant.pokemon.name} has fainted!")
            player_1.swap_pokemon(player_2.participant)
        if not player_2.participant.is_alive:
            self.message_queue.append(f"{player_2.participant.pokemon.name} has fainted!")
            player_2.swap_pokemon(player_1.participant)
        self.message_queue.append(f"Round: {self.round_number:02d} completed!")
        if self.display_messages:
            self.message_queue.append("")
            for message in self.message_queue:
                print(message)
        self.message_queue.clear()
        self.message_queue.append("")
