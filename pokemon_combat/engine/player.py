from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pokemon_combat.engine.participant import Participant
from pokemon_combat.moves.move import Move
from pokemon_combat.pokemon.pokemon import Pokemon


class Player(ABC):
    def __init__(self, pokemon_team: List[Pokemon]):
        self.participant = Participant()
        # TODO: Add team information here
        self.pokemon_team: Dict[str, Pokemon] = {pokemon.name: pokemon for pokemon in pokemon_team}
        
    @abstractmethod
    def make_move(self, opponent: Participant) -> Move:
        pass
    
    @abstractmethod
    def choose_next_pokemon(self, opponent: Optional[Participant]) -> Pokemon:
        pass
    
    def swap_pokemon(self, opponent: Optional[Participant]):
        self.participant.remove_pokemon()
        next_pokemon = self.choose_next_pokemon(opponent)
        self.participant.add_pokemon(next_pokemon)
        
    def alive_pokemon(self) -> List[Pokemon]:
        return [pokemon for pokemon in self.pokemon_team.values() if pokemon.is_alive]