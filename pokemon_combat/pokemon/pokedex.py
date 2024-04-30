from dataclasses import dataclass
from pathlib import Path
from json import load
from typing import Optional, Tuple, Dict, Any, Set
from typing_extensions import Self
from os import listdir
from pokemon_combat.pokemon.pokemon_base_stats import PokemonBaseStats
from pokemon_combat.pokemon.pokemon_types import PokemonTypeEnum
from pokemon_combat.pokemon.individual_values import IndividualValues
from pokemon_combat.pokemon.effort_values import EffortValues
from pokemon_combat.pokemon.pokemon_natures import PokemonNatureEnum
from pokemon_combat.pokemon.pokemon import Pokemon
from pokemon_combat.moves.move import Move


@dataclass
class PokedexEntry:
    name: str
    elements: Tuple[PokemonTypeEnum, Optional[PokemonTypeEnum]]
    base_stats: PokemonBaseStats

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> Self:
        for n, element in enumerate(config['elements']):
            val = None if element is None else PokemonTypeEnum[element]
            config['elements'][n] = val
        config['elements'] = tuple(config['elements'])
        config['base_stats'] = PokemonBaseStats.from_dict(config['base_stats'])
        return cls(**config)
    
    @classmethod
    def from_json(cls, path: Path) -> Self:
        with open(path, 'r') as infile:
            config = load(infile)
        return cls.from_dict(config)
    
    def make_pokemon(self, level: int, individual_values: IndividualValues, effort_values: EffortValues, 
                     nature: PokemonNatureEnum, moves: Tuple[Move, Optional[Move], Optional[Move], Optional[Move]]) -> Pokemon:
        return Pokemon(self.name, level, self.base_stats, individual_values, effort_values, nature, self.elements, 
                       moves)

class Pokedex:
    def __init__(self, data_path: Path):
        assert data_path.exists(), f"Path to pokemon data {data_path} is invalid"
        self.data_path = data_path
        available_pokemon = [f for f in listdir(str(data_path)) if f.split('.')[-1] == 'json']
        self._pokemon = {ap.split('.')[0]: PokedexEntry.from_json(self.data_path / ap) for ap in available_pokemon}
    
    @property
    def available_pokemon(self) -> Set[str]:
        return set(self._pokemon.keys())
    
    def get(self, pokemon_name: str) -> PokedexEntry:
        stats = self._pokemon.get(pokemon_name, None)
        if stats is None:
            raise ValueError(f"Can not get data for pokemon : {pokemon_name} as it is not in the pokedex.")
        return stats