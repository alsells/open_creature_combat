from typing import Optional, List
from creature_combat.engine.player import Player
from creature_combat.engine.participant import Participant
from creature_combat.engine.combat_functions import get_type_modifier
from creature_combat.creature.creature import Creature
from creature_combat.moves.move import Move


class SuperEffectivePlayer(Player):
    def choose_next_creature(self, opponent: Optional[Participant]) -> Creature:
        available_creature = self.alive_creature()
        for creature in available_creature:
            if opponent is None:
                return creature
            else:
                if any([get_type_modifier(move, opponent) > 1.0 for move in creature._moves]):
                    return creature
        else:
            return available_creature[0] if len(available_creature) > 0 else None
        
    def make_move(self, opponent: Participant) -> Move:
        mutable_moves: List[Move] = list(self.participant.creature._moves)
        mutable_moves = [mm for mm in mutable_moves if mm is not None]
        mutable_moves.sort(key=lambda m: 0 if m.power is None else m.power, reverse=True)
        for move in mutable_moves:
            if self.participant.can_make_move(move.name):
                if get_type_modifier(move, opponent) > 1.0:
                    return self.participant.make_move(move.name)
        else:
            return self.participant.make_move(mutable_moves[0].name)
        
        
class TextBasePlayer(Player):
    def choose_next_creature(self, opponent: Participant | None) -> Creature:
        options = self.alive_creature()
        poke_string = ""
        for n, opt in enumerate(options):
            poke_string += f"Type: {n} for {opt.name}\n"
        prompt = "Select next creature:\n" + poke_string
        choice = None
        while choice is None:
            choice = input(prompt)
            try:
                choice = int(choice)
                if choice >= len(options):
                    print(f"{choice} is not a valid creature to choose. Please select again.")
                    choice = None
            except ValueError:
                print(f'Please enter an integer between [0-{len(options)-1}]')
                choice = None
        return options[choice]
    
    def make_move(self, opponent: Participant) -> Move:
        msg = "Remaining PP:\n"
        for move_name, remaining_pp in self.participant.creature._remaining_pp.items():
            msg += f"{move_name}: {remaining_pp} / {self.participant.creature._move_map[move_name].max_pp}\n"
        print(msg)
        choice = None
        move_string = ""
        for n, move in enumerate(self.participant.creature._moves):
            if move is not None:
                move_string += f"Type: {n} for {move.name}\n" 
        prompt = f"Select what move {self.participant.creature.name} should use:\n" + move_string
        while choice is None:
            choice = input(prompt)
            try:
                choice = int(choice)
                if choice >= len(self.participant.creature._moves):
                    print(f'Please enter an integer between [0-3]')
                    choice = None
                else:
                    can_make = self.participant.can_make_move(self.participant.creature._moves[choice].name)
                    if not can_make:
                        print(f"Choice: {self.participant.creature._moves[choice]} is not a valid move in {self.participant.creature.name}'s move list. Please pick a different option.")
                        choice = None
            except ValueError:
                print(f'Please enter an integer between [0-3]')
                choice = None
        rval = self.participant.make_move(self.participant.creature._moves[choice].name)
        return rval