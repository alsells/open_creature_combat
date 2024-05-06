from pathlib import Path
from creature_combat.creature.creaturedex import CreatureDex
from creature_combat.creature.effort_values import EffortValues
from creature_combat.creature.individual_values import IndividualValues
from creature_combat.creature.creature_natures import CreatureNatureEnum
from creature_combat.moves.move_list import MoveList
from creature_combat.engine.combat_manager import CombatManager

from demo_players import TextBasePlayer, SuperEffectivePlayer

def main():
    here = Path(__file__)
    top = here.parent.parent
    creaturedex_path = top / "creaturedex_data"
    if not creaturedex_path.exists():
        raise RuntimeError(f"Could not find creature dex path @: {creaturedex_path}")
    movedata_path = top / "move_data"
    if not movedata_path.exists():
        raise RuntimeError(f"Could not find move list path @: {movedata_path}")
    creaturedex = CreatureDex(creaturedex_path)
    movelist = MoveList(movedata_path)
    bulbasaur_entry = creaturedex.get('Bulbasaur')
    bulbasaur_moves = (movelist.get('Tackle'),movelist.get('Growl'),movelist.get('Vine Whip'),None)
    bulbasaur_ev = EffortValues.make_random()
    bulbasaur_iv = IndividualValues.make_random()
    bulbasaur_nature = CreatureNatureEnum.MILD
    bulbasaur_level = 5
    bulbasaur = bulbasaur_entry.make_creature(bulbasaur_level, bulbasaur_iv, bulbasaur_ev, bulbasaur_nature, bulbasaur_moves)
    player_1_team = [bulbasaur]
    player_1 = TextBasePlayer(player_1_team)
    squirtle_entry = creaturedex.get('Squirtle')
    squirtle_moves = (movelist.get('Tackle'),movelist.get('Tail Whip'),movelist.get('Water Gun'),None)
    squirtle_ev = EffortValues.make_random()
    squirtle_iv = IndividualValues.make_random()
    squirtle_nature = CreatureNatureEnum.HARDY
    squirtle_level = 5
    squirtle = squirtle_entry.make_creature(squirtle_level, squirtle_iv, squirtle_ev, squirtle_nature, squirtle_moves)
    player_2_team = [squirtle]
    player_2 = SuperEffectivePlayer(player_2_team)
    manager = CombatManager(True)
    manager.reset(player_1, player_2)
    while len(player_1.alive_creature()) > 0 and len(player_2.alive_creature()) > 0:
        manager.step_round(player_1, player_2)
    win = len(player_1.alive_creature()) > 0
    if win:
        print("Congratulation on your win! Run to try again.")
    else:
        print("Better luck next time. Run to try again.")

if __name__ == "__main__":
    main()