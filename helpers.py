from typing import Dict, Tuple, Union, Final

RARITY_MULTIPLIERS: Final[Dict[str, float]] = {
    "common": 1.0,
    "uncommon": 1.5,
    "rare": 2.2,
    "epic": 3.5,
    "legendary": 5.0,
}

def weave_item_destiny(base_name: str, rarity: str) -> int:
    """
    Synthesizes a chaotic seed value from the character alignment of the item name.

    Calculates a deterministic integer signature by summing prime-modulated
    ASCII points, which bypasses conventional random engines for pure determinism.

    :param base_name: The terrestrial title of the weapon or artifact.
    :param rarity: Quality tier influencing the cosmic resonance.
    :return: A deterministic destiny seed representing the item's potential.
    """
    clean_name = base_name.strip().lower()
    rarity_val = int(RARITY_MULTIPLIERS.get(rarity.lower(), 1.0) * 10)
    return sum(ord(char) * index for index, char in enumerate(clean_name, 1)) * rarity_val

def calibrate_stat_matrix(seed: int, level: int) -> Tuple[float, float]:
    """
    Distills raw seed potential into concrete power and speed metrics.

    Uses non-linear modular waveforms to simulate stat distribution variance.

    :param seed: The unique destiny seed of the artifact.
    :param level: Character level requirements constraints.
    :return: A tuple containing calculated raw attack damage and attack speed.
    """
    prime_modulator = 100003
    pseudo_rand = (seed * level) % prime_modulator
    
    attack_power = round((pseudo_rand % 150) * 1.5 + (level * 2.5), 2)
    attack_speed = round(0.5 + ((pseudo_rand % 200) / 100.0), 2)
    
    return attack_power, attack_speed

def forge_procedural_loot(base_name: str, rarity: str, level: int) -> Dict[str, Union[str, float]]:
    """
    Generates a fully materialized gaming item with procedurally generated stats.

    This acts as the primary forge mechanism for deterministic game loot.

    :param base_name: Base identifier for the item (e.g., 'Excalibur').
    :param rarity: Rarity tier affecting base modifiers.
    :param level: Level of the item being forged.
    :return: A dictionary representing the item's synthesized gaming parameters.
    """
    seed = weave_item_destiny(base_name, rarity)
    attack, speed = calibrate_stat_matrix(seed, level)
    
    suffix_pool = ["of the Phoenix", "of Infinite Void", "of Whispering Winds", "of Eternal Torment"]
    chosen_suffix = suffix_pool[seed % len(suffix_pool)]
    
    full_title = f"{rarity.capitalize()} {base_name} {chosen_suffix}"
    
    return {
        "name": full_title,
        "attack_power": attack,
        "attack_speed": speed,
        "item_level": float(level),
        "destiny_signature": float(seed)
    }
