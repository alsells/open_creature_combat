import pytest
from pathlib import Path
from ..pokemon_combat.pokemon.pokedex import Pokedex
from ..pokemon_combat.pokemon.effort_values import EffortValues
from ..pokemon_combat.pokemon.individual_values import IndividualValues
from ..pokemon_combat.pokemon.pokemon_natures import PokemonNatureEnum
from ..pokemon_combat.moves.move_list import MoveList

_POKEDEX_PATH = Path(r"..\pokedex_data")
_MOVE_LIST_PATH = Path(r"..\move_data")

class TestStatInitialization:
    _BULBASAUR_MINIMUMS = [200, 92, 92, 121, 121, 85]
    _BULBASAUR_MAXIMUMS = [294, 216, 216, 251, 251, 207]
    _POKEDEX = Pokedex(_POKEDEX_PATH)
    _MOVE_LIST = MoveList(_MOVE_LIST_PATH)
    
    def test_hp_min(self):
        level = 100
        bulbasaur_entry = self._POKEDEX.get('Bulbasaur')
        bulbasaur = bulbasaur_entry.make_pokemon(level, IndividualValues.make_zero(), EffortValues.make_zero(), PokemonNatureEnum.BASHFUL,
                                                 (self._MOVE_LIST.get('Tackle'),None,None,None))
        assert bulbasaur.max_hp == self._BULBASAUR_MINIMUMS[0]