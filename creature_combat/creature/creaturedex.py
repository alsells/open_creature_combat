from dataclasses import dataclass
from pathlib import Path
from json import load
from typing import Optional, Tuple, Dict, Any, Set
from typing_extensions import Self
from os import listdir
from creature_combat.creature.creature_base_stats import CreatureBaseStats
from creature_combat.creature.creature_types import CreatureTypeEnum
from creature_combat.creature.individual_values import IndividualValues
from creature_combat.creature.effort_values import EffortValues
from creature_combat.creature.creature_natures import CreatureNatureEnum
from creature_combat.creature.creature import Creature
from creature_combat.moves.move import Move


@dataclass
class CreatureEntry:
    name: str
    elements: Tuple[CreatureTypeEnum, Optional[CreatureTypeEnum]]
    base_stats: CreatureBaseStats

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> Self:
        for n, element in enumerate(config['elements']):
            val = None if element is None else CreatureTypeEnum[element]
            config['elements'][n] = val
        config['elements'] = tuple(config['elements'])
        config['base_stats'] = CreatureBaseStats.from_dict(config['base_stats'])
        return cls(**config)
    
    @classmethod
    def from_json(cls, path: Path) -> Self:
        with open(path, 'r') as infile:
            config = load(infile)
        return cls.from_dict(config)
    
    def make_creature(self, level: int, individual_values: IndividualValues, effort_values: EffortValues, 
                     nature: CreatureNatureEnum, moves: Tuple[Move, Optional[Move], Optional[Move], Optional[Move]]) -> Creature:
        return Creature(self.name, level, self.base_stats, individual_values, effort_values, nature, self.elements, 
                       moves)


class CreatureDex:
    def __init__(self, data_path: Path):
        assert data_path.exists(), f"Path to creature data {data_path} is invalid"
        self.data_path = data_path
        available_creature = [f for f in listdir(str(data_path)) if f.split('.')[-1] == 'json']
        self._creature = {ap.split('.')[0]: CreatureEntry.from_json(self.data_path / ap) for ap in available_creature}
    
    @property
    def available_creature(self) -> Set[str]:
        return set(self._creature.keys())
    
    def get(self, creature_name: str) -> CreatureEntry:
        stats = self._creature.get(creature_name, None)
        if stats is None:
            raise ValueError(f"Can not get data for creature : {creature_name} as it is not in the creature dex.")
        return stats