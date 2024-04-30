from typing import Optional, List
from pokemon_combat.engine.player import Player
from pokemon_combat.engine.participant import Participant
from pokemon_combat.engine.combat_functions import get_type_modifier
from pokemon_combat.pokemon.pokemon import Pokemon
from pokemon_combat.moves.move import Move


class SuperEffectivePlayer(Player):
    def choose_next_pokemon(self, opponent: Optional[Participant]) -> Pokemon:
        available_pokemon = self.alive_pokemon()
        for pokemon in available_pokemon:
            if opponent is None:
                return pokemon
            else:
                if any([get_type_modifier(move, opponent) > 1.0 for move in pokemon._moves]):
                    return pokemon
        else:
            return available_pokemon[0] if len(available_pokemon) > 0 else None
        
    def make_move(self, opponent: Participant) -> Move:
        mutable_moves: List[Move] = list(self.participant.pokemon._moves)
        mutable_moves = [mm for mm in mutable_moves if mm is not None]
        mutable_moves.sort(key=lambda m: 0 if m.power is None else m.power, reverse=True)
        for move in mutable_moves:
            if self.participant.can_make_move(move.name):
                if get_type_modifier(move, opponent) > 1.0:
                    return self.participant.make_move(move.name)
        else:
            return self.participant.make_move(mutable_moves[0].name)
        
        
class TextBasePlayer(Player):
    def choose_next_pokemon(self, opponent: Participant | None) -> Pokemon:
        options = self.alive_pokemon()
        poke_string = ""
        for n, opt in enumerate(options):
            poke_string += f"Type: {n} for {opt.name}\n"
        prompt = "Select next Pokemon:\n" + poke_string
        choice = None
        while choice is None:
            choice = input(prompt)
            try:
                choice = int(choice)
                if choice >= len(options):
                    print(f"{choice} is not a valid pokemon to choose. Please select again.")
                    choice = None
            except ValueError:
                print(f'Please enter an integer between [0-{len(options)-1}]')
                choice = None
        return options[choice]
    
    def make_move(self, opponent: Participant) -> Move:
        msg = "Remaining PP:\n"
        for move_name, remaining_pp in self.participant.pokemon._remaining_pp.items():
            msg += f"{move_name}: {remaining_pp} / {self.participant.pokemon._move_map[move_name].max_pp}\n"
        print(msg)
        choice = None
        move_string = ""
        for n, move in enumerate(self.participant.pokemon._moves):
            if move is not None:
                move_string += f"Type: {n} for {move.name}\n" 
        prompt = f"Select what move {self.participant.pokemon.name} should use:\n" + move_string
        while choice is None:
            choice = input(prompt)
            try:
                choice = int(choice)
                if choice >= len(self.participant.pokemon._moves):
                    print(f'Please enter an integer between [0-3]')
                    choice = None
                else:
                    can_make = self.participant.can_make_move(self.participant.pokemon._moves[choice].name)
                    if not can_make:
                        print(f"Choice: {self.participant.pokemon._moves[choice]} is not a valid move in {self.participant.pokemon.name}'s move list. Please pick a different option.")
                        choice = None
            except ValueError:
                print(f'Please enter an integer between [0-3]')
                choice = None
        rval = self.participant.make_move(self.participant.pokemon._moves[choice].name)
        return rval