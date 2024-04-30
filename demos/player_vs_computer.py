from pathlib import Path
from pokemon_combat.pokemon.pokedex import Pokedex
from pokemon_combat.pokemon.effort_values import EffortValues
from pokemon_combat.pokemon.individual_values import IndividualValues
from pokemon_combat.pokemon.pokemon_natures import PokemonNatureEnum
from pokemon_combat.moves.move_list import MoveList
from pokemon_combat.engine.combat_manager import CombatManager

from demo_players import TextBasePlayer, SuperEffectivePlayer

def main():
    pokedex = Pokedex(Path(r"D:\Documents\build\poke-ml\open_pokemon_combat\pokedex_data"))
    movelist = MoveList(Path(r"D:\Documents\build\poke-ml\open_pokemon_combat\move_data"))
    bulbasaur_entry = pokedex.get('Bulbasaur')
    bulbasaur_moves = (movelist.get('Tackle'),movelist.get('Growl'),movelist.get('Vine Whip'),None)
    bulbasaur_ev = EffortValues.make_random()
    bulbasaur_iv = IndividualValues.make_random()
    bulbasaur_nature = PokemonNatureEnum.MILD
    bulbasaur_level = 5
    bulbasaur = bulbasaur_entry.make_pokemon(bulbasaur_level, bulbasaur_iv, bulbasaur_ev, bulbasaur_nature, bulbasaur_moves)
    player_1_team = [bulbasaur]
    player_1 = TextBasePlayer(player_1_team)
    squirtle_entry = pokedex.get('Squirtle')
    squirtle_moves = (movelist.get('Tackle'),movelist.get('Tail Whip'),movelist.get('Water Gun'),None)
    squirtle_ev = EffortValues.make_random()
    squirtle_iv = IndividualValues.make_random()
    squirtle_nature = PokemonNatureEnum.HARDY
    squirtle_level = 5
    squirtle = squirtle_entry.make_pokemon(squirtle_level, squirtle_iv, squirtle_ev, squirtle_nature, squirtle_moves)
    player_2_team = [squirtle]
    player_2 = SuperEffectivePlayer(player_2_team)
    manager = CombatManager(True)
    manager.reset(player_1, player_2)
    while len(player_1.alive_pokemon()) > 0 and len(player_2.alive_pokemon()) > 0:
        manager.take_turn(player_1, player_2)
    win = len(player_1.alive_pokemon()) > 0
    if win:
        print("Congradulations on your win! Run to try again.")
    else:
        print("Better luck next time. Run to try again.")

if __name__ == "__main__":
    main()