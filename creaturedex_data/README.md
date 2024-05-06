# Creature Dex Entry Fields:

- "name": Name of the Creature 
- "elements": Either 1 or 2 elements from the following list, use null for element 2 if only 1 present
    - NORMAL, FIRE, WATER, ELECTRIC, GRASS, ICE, FIGHTING, POISON, GROUND, FLYING, PSYCHIC, BUG, ROCK, GHOST, DRAGON, DARK, STEEL, FAIRY
- "base_stats": Dictionary of the base stats for the creature containing the following fields:
    - "health_points": Base stat used for calculating the max health points for the creature
    - "physical_attack": Base stat used for calculating the physical attack for the creature
    - "physical_defense": Base stat used for calculating the physical defense for the creature
    - "special_attack": Base stat used for calculating the special attack for the creature
    - "special_defense": Base stat used for calculating the special defense for the creature
    - "speed": Base stat used for calculating the speed for the creature