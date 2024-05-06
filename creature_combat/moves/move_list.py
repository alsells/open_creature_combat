from pathlib import Path
from os import listdir
from typing import Set
from creature_combat.moves.move import Move


class MoveList:
    def __init__(self, data_path: Path):
        assert data_path.exists(), f"Path to Move list data {data_path} is invalid"
        self.data_path = data_path
        available_moves = [f for f in listdir(str(data_path)) if f.split('.')[-1] == 'json']
        self._moves = {am.split('.')[0]: Move.from_json(self.data_path / am) for am in available_moves}
        
    @property
    def available_moves(self) -> Set[str]:
        """Lists the Moves that have been loaded into the MoveList

        Returns:
            Set[str]: Names of all of the Moves available in the MoveList
        """
        return set(self._moves.keys())
    
    def get(self, move_name: str) -> Move:
        """Accessor method for the _moves dictionary stored in the MoveList. Primarily wraps the dictionary .get() method to return a more explicit error when it errors out.

        Args:
            move_name (str): Name of the move to get the Move for.

        Raises:
            ValueError: If the move_name isn't in the _creature dictionary 

        Returns:
            Move: Move instance for the requested move_name
        """
        move = self._moves.get(move_name, None)
        if move is None:
            raise ValueError(f"Can not get data for move: {move_name} as it is not in the move list.")
        return move
    