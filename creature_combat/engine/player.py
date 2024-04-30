from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from creature_combat.engine.participant import Participant
from creature_combat.moves.move import Move
from creature_combat.creature.creature import creature


class Player(ABC):
    def __init__(self, creature_team: List[creature]):
        self.participant = Participant()
        # TODO: Add team information here
        self.creature_team: Dict[str, creature] = {creature.name: creature for creature in creature_team}
        
    @abstractmethod
    def make_move(self, opponent: Participant) -> Move:
        pass
    
    @abstractmethod
    def choose_next_creature(self, opponent: Optional[Participant]) -> creature:
        pass
    
    def swap_creature(self, opponent: Optional[Participant]):
        self.participant.remove_creature()
        next_creature = self.choose_next_creature(opponent)
        self.participant.add_creature(next_creature)
        
    def alive_creature(self) -> List[creature]:
        return [creature for creature in self.creature_team.values() if creature.is_alive]