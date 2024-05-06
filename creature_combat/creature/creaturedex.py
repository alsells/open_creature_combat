from __future__ import annotations
from dataclasses import dataclass
from json import load
from os import listdir
from creature_combat.creature.creature_base_stats import CreatureBaseStats
from creature_combat.creature.creature_types import CreatureTypeEnum
from creature_combat.creature.creature import Creature
from creature_combat.utils import annotations as anno


@dataclass
class CreatureEntry:
    """Data container for the immutable attributes of a Creature"""
    name: str  # Name of the Creature
    elements: anno.Tuple[CreatureTypeEnum, anno.Optional[CreatureTypeEnum]]  # What Element is the Creature
    base_stats: CreatureBaseStats  # The base statistics of the Creature

    @classmethod
    def from_dict(cls, config: anno.Config) -> anno.Self:
        """Parses a config dictionary, and formats the data to create an instance of CreatureEntry.

        Args:
            config (Dict[str, Any]): Dictionary containing attribute names and values for CreatureEntry

        Returns:
            Self: Instance of CreatureEntry
        """
        # Iterate through all of the elements to instantiate them 
        for n, element in enumerate(config['elements']):
            val = None if element is None else CreatureTypeEnum[element]
            config['elements'][n] = val
        config['elements'] = tuple(config['elements'])
        config['base_stats'] = CreatureBaseStats.from_dict(config['base_stats'])
        return cls(**config)
    
    @classmethod
    def from_json(cls, path: anno.Path) -> anno.Self:
        """Generates a CreatureEntry from a json file provided at path.

        Args:
            path (Path): Path to the creature entry config file.

        Returns:
            Self: Instance of CreatureEntry
        """
        with open(path, 'r') as infile:
            config = load(infile)
        return cls.from_dict(config)
    
    def make_creature(self, level: int, individual_values: anno.IndividualValues, effort_values: anno.EffortValues, 
                     nature: anno.CreatureNatureEnum, moves: anno.Moves) -> Creature:
        """Makes a Creature object based on this CreatureEntry, as well as the mutable parameters of level, EVs, IVs, nature, and moves

        Args:
            level (int): What level of Creature to make
            individual_values (IndividualValues): IVs for the Creature
            effort_values (EffortValues): EVs for the Creature
            nature (CreatureNatureEnum): Nature of the Creature
            moves (Tuple[Move, Optional[Move], Optional[Move], Optional[Move]]): List of moves the Creature has

        Returns:
            Creature: Instance of a Creature object based on provided values
        """
        return Creature(self.name, level, self.base_stats, individual_values, effort_values, nature, self.elements, moves)


class CreatureDex:
    def __init__(self, data_path: anno.Path):
        assert data_path.exists(), f"Path to creature data {data_path} is invalid"
        self.data_path = data_path
        available_creature = [f for f in listdir(str(data_path)) if f.split('.')[0] != 'example' and f.split('.')[-1] == 'json']
        self._creature = {ap.split('.')[0]: CreatureEntry.from_json(self.data_path / ap) for ap in available_creature}
    
    @property
    def available_creature(self) -> anno.Set[str]:
        """Lists the Creatures that have been loaded into the CreatureDex currently

        Returns:
            Set[str]: Set of the Creature Names available in the CreatureDex
        """
        return set(self._creature.keys())
    
    def get(self, creature_name: str) -> CreatureEntry:
        """Accessor method for the _creature dictionary stored in the CreatureDex. Primarily wraps the dictionary .get() method to return a more explicit error when it errors out.

        Args:
            creature_name (str): Name of the creature to get the CreatureEntry for.

        Raises:
            ValueError: If the creature_name isn't in the _creature dictionary 

        Returns:
            CreatureEntry: CreatureEntry instance for the requested creature_name
        """
        stats = self._creature.get(creature_name, None)
        if stats is None:
            raise ValueError(f"Can not get data for creature : {creature_name} as it is not in the creature dex.")
        return stats