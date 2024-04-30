from dataclasses import dataclass
from typing_extensions import Self
from numpy.random import randint


@dataclass
class EffortValues:
    health_point: int
    physical_attack: int
    physical_defense: int
    special_attack: int
    special_defense: int
    speed: int
    
    def __post_init__(self):
        assert 0<=self.health_point<252, f"Health point IVs must be between [0-252], IV was provided as {self.health_point}."
        assert 0<=self.physical_attack<252, f"Physical attack IVs must be between [0-252], IV was provided as {self.physical_attack}."
        assert 0<=self.physical_defense<252, f"Physical defense IVs must be between [0-252], IV was provided as {self.physical_defense}."
        assert 0<=self.special_attack<252, f"Special attack IVs must be between [0-252], IV was provided as {self.special_attack}."
        assert 0<=self.special_defense<252, f"Special defense IVs must be between [0-252], IV was provided as {self.special_defense}."
        assert 0<=self.speed<252, f"Speed IVs must be between [0-252], IV was provided as {self.speed}."
        ev_total = self.health_point+self.physical_attack+self.physical_defense+self.special_attack+self.special_defense+self.speed
        assert ev_total <= 510, f"Total EVs must be less than 510, provided {ev_total}. Please decrease EVs to a valid range"
        
    @classmethod
    def make_zero(cls) -> Self:
        return cls(0, 0, 0, 0, 0, 0)
    
    @classmethod
    def make_random(cls) -> Self:
        return cls(randint(0, 80), randint(0, 80), randint(0, 80), randint(0, 80), randint(0, 80), randint(0, 80))