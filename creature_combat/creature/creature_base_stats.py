from __future__ import annotations
from dataclasses import dataclass
from numpy import uint8

from creature_combat.utils import annotations as anno


@dataclass
class CreatureBaseStats:
    health_points: uint8
    physical_attack: uint8
    physical_defense: uint8
    special_attack: uint8
    special_defense: uint8
    speed: uint8
    
    @classmethod
    def from_dict(cls, config: anno.Dict[str, int]) -> anno.Self:
        """Method to create an instance of CreatureBaseStats with data contained within a python dictionary. Converts input values into uint8 values

        Args:
            config (Dict[str, int]): Mapping of attribute names to the values for those attributes for this object instance.

        Returns:
            Self: An instance of CreatureBaseStats with the specified values.
        """
        config['health_points'] = uint8(config['health_points'])
        config['physical_attack'] = uint8(config['physical_attack'])
        config['physical_defense'] = uint8(config['physical_defense'])
        config['special_attack'] = uint8(config['special_attack'])
        config['special_defense'] = uint8(config['special_defense'])
        config['speed'] = uint8(config['speed'])
        return cls(**config)
        
    def __post_init__(self):
        assert isinstance(self.health_points, uint8), f"Health points provided as {type(self.health_points)} expected uint8"
        assert isinstance(self.physical_attack, uint8), f"Physical attack provided as {type(self.physical_attack)} expected uint8"
        assert isinstance(self.physical_defense, uint8), f"Physical defense provided as {type(self.physical_defense)} expected uint8"
        assert isinstance(self.special_attack, uint8), f"Special attack provided as {type(self.special_attack)} expected uint8"
        assert isinstance(self.special_defense, uint8), f"Special defense provided as {type(self.special_defense)} expected uint8"
        assert isinstance(self.speed, uint8), f"Speed provided as {type(self.speed)} expected uint8"