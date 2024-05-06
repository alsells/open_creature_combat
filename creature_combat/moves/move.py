from dataclasses import dataclass, field
from json import load
from pathlib import Path
from typing import Optional, List, Dict, Any
from typing_extensions import Self
from creature_combat.moves.move_effects import MoveEffectEnum
from creature_combat.moves.move_types import MoveTypeEnum
from creature_combat.creature.creature_types import CreatureTypeEnum


@dataclass
class Move:
    name: str
    move_type: MoveTypeEnum
    element: CreatureTypeEnum
    power: Optional[int]
    accuracy: Optional[int]
    high_crit_flag:bool
    max_pp: int
    priority: int=0
    self_effect: List[str]=field(default_factory=list)
    opponent_effect: List[str]=field(default_factory=list)
    environment_effect: List[str]=field(default_factory=list)

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> Self:
        config['move_type'] = MoveTypeEnum.init_from_key_or_value(config['move_type'])
        config['element'] = CreatureTypeEnum.init_from_key_or_value(config['element'])
        return cls(**config)
    
    @classmethod
    def from_json(cls, path: Path) -> Self:
        with open(path, 'r') as infile:
            config = load(infile)
        return cls.from_dict(config)

    @property
    def is_attack(self) -> bool:
        return self.move_type != MoveTypeEnum.STATUS

    def __hash__(self) -> int:
        return hash(self.name)