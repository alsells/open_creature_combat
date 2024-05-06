from __future__ import annotations
from abc import ABC, abstractmethod

from creature_combat.engine.participant import Participant
from creature_combat.utils import annotations as anno


class Player(ABC):
    def __init__(self, creature_team: anno.Creatures):
        self.participant = Participant()
        self.creature_team: anno.Team = {creature.name: creature for creature in creature_team}
        
    @abstractmethod
    def select_move(self, opponent: Participant) -> str:
        """Selects what move of the available moves to use for this round of combat.

        Args:
            opponent (Participant): The opponent this player is going against.

        Returns:
            str: Name of the move to use 
        """
        pass
        
    def make_move(self, opponent: Participant) -> anno.Move:
        """Makes the selected move for the current round in combat. Calls the owned participants make_move method to ensure all updates are propagated.

        Args:
            opponent (Participant): The opponent this player is going against

        Returns:
            Move: What move is used by this player this round.
        """
        move_name = self.select_move(opponent)
        return self.participant.make_move(move_name)
    
    @abstractmethod
    def choose_next_creature(self, opponent: anno.Optional[Participant]) -> anno.Creature:
        """Chooses what creature to use based on what this player is going against.

        Args:
            opponent (Optional[Participant]): What participant is the player going up against. At match start there may not be a participant.

        Returns:
            Creature: What creature to use in combat next
        """
        pass
    
    def swap_creature(self, opponent: anno.Optional[Participant]):
        """Removes the current creature, chooses the next creature to use based on the opponent, and then adds the selected creature to the participant.

        Args:
            opponent (Optional[Participant]): What participant the player is going up against. At match start there may not be a participant.
        """
        self.participant.remove_creature()
        next_creature = self.choose_next_creature(opponent)
        self.participant.add_creature(next_creature)
        
    def alive_creature(self) -> anno.Creatures:
        """Returns the list of available creatures to use by this player.

        Returns:
            List[Creature]: List of available creatures if they are alive
        """
        return [creature for creature in self.creature_team.values() if creature.is_alive]