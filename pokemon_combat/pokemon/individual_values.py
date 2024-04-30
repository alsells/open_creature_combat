from dataclasses import dataclass
from numpy.random import randint
from typing_extensions import Self


@dataclass
class IndividualValues:
    health_point: int
    physical_attack: int
    physical_defense: int
    special_attack: int
    special_defense: int
    speed: int
    
    def __post_init__(self):
        assert 0<=self.health_point<32, f"Health point IVs must be between [0-31], IV was provided as {self.health_point}."
        assert 0<=self.physical_attack<32, f"Physical attack IVs must be between [0-31], IV was provided as {self.physical_attack}."
        assert 0<=self.physical_defense<32, f"Physical defense IVs must be between [0-31], IV was provided as {self.physical_defense}."
        assert 0<=self.special_attack<32, f"Special attack IVs must be between [0-31], IV was provided as {self.special_attack}."
        assert 0<=self.special_defense<32, f"Special defense IVs must be between [0-31], IV was provided as {self.special_defense}."
        assert 0<=self.speed<32, f"Speed IVs must be between [0-31], IV was provided as {self.speed}."
        
    @classmethod
    def make_zero(cls) -> Self:
        return cls(0, 0, 0, 0, 0, 0)
    
    @classmethod
    def make_random(cls) -> Self:
        return cls(randint(0, 32), randint(0, 32), randint(0, 32), randint(0, 32), randint(0, 32), randint(0, 32))