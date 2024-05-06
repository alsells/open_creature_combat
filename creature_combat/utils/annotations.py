import typing

if typing.TYPE_CHECKING:
    # Package Imports
    from numpy import ndarray
    from pathlib import Path
    from typing import *
    from typing_extensions import Self
    
    # Creature Imports
    from creature_combat.creature.creature import Creature
    from creature_combat.creature.creature_base_stats import CreatureBaseStats
    from creature_combat.creature.creature_natures import CreatureNatureEnum
    from creature_combat.creature.creature_types import CreatureTypeEnum
    from creature_combat.creature.creaturedex import CreatureDex, CreatureEntry
    from creature_combat.creature.effort_values import EffortValues
    from creature_combat.creature.individual_values import IndividualValues
    
    # Engine Imports
    from creature_combat.engine.combat_manager import CombatManager
    from creature_combat.engine.participant import Participant
    from creature_combat.engine.player import Player
    
    # Item Imports
    
    # Move Imports
    from creature_combat.moves.move import Move
    from creature_combat.moves.move_list import MoveList
    from creature_combat.moves.move_types import MoveTypeEnum
    
    # Statuses Imports
    from creature_combat.statuses.non_volatile_statuses import NonVolatileStatusEnum
    
    # Utils Imports
    from creature_combat.utils.extended_enums import ExtendedEnum
    
    # Project Composite annotations
    Config = Dict[str, Any]
    Moves = Tuple[Move,Optional[Move],Optional[Move],Optional[Move]]
    Creatures = List[Creature]
    Team = Dict[str, Creature]