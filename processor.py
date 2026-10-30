import random
import time

def loot_generator(rarity_table):
    target = random.random()
    accumulator = 0.0
    for item, chance in rarity_table.items():
        accumulator += chance
        if target <= accumulator:
            return item
    return list(rarity_table.keys())[-1]

def cooldown_tracker(last_cast, duration):
    return time.time() - last_cast >= duration

def normalize_stats(stats, target_sum):
    total = sum(stats.values())
    if total == 0:
        return {k: target_sum // len(stats) for k in stats}
    return {k: int((v / total) * target_sum) for k, v in stats.items()}

def packet_throttler(queue, max_size=64):
    return queue[-max_size:]

def calculate_dps(damage_dealt, duration):
    return round(damage_dealt / duration, 2) if duration > 0 else 0.0

def sequence_buffer(history, new_input, limit=10):
    history.append(new_input)
    return history[-limit:]