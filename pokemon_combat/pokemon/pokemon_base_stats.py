from typing_extensions import Self
from typing import Dict
from numpy import uint8
from dataclasses import dataclass


@dataclass
class PokemonBaseStats:
    health_points: uint8
    physical_attack: uint8
    physical_defense: uint8
    special_attack: uint8
    special_defense: uint8
    speed: uint8
    
    @classmethod
    def from_dict(cls, config: Dict[str, int]) -> Self:
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