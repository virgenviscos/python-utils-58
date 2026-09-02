from collections import defaultdict
from typing import List, Dict, Any, Callable

def create_gaming_data_handler() -> Callable:
    state = {
        'total_score': 0,
        'combos': {},
        'inventory': defaultdict(int),
        'events': []
    }

    def handler(command: str, *args) -> Any:
        if command == 'add_score':
            amount = args[0] if args else 0
            state['total_score'] += amount
            state['events'].append(('score', amount))
            return state['total_score']
        elif command == 'apply_combo':
            combo_type = args[0] if args else 'default'
            multiplier = args[1] if len(args) > 1 else 2
            if combo_type in state['combos']:
                state['combos'][combo_type] += 1
            else:
                state['combos'][combo_type] = 1
            bonus = state['combos'][combo_type] * multiplier
            state['total_score'] += bonus
            state['events'].append(('combo', combo_type, bonus))
            return bonus
        elif command == 'add_item':
            item = args[0] if args else 'unknown'
            quantity = args[1] if len(args) > 1 else 1
            state['inventory'][item] += quantity
            state['events'].append(('item', item, quantity))
            return state['inventory'][item]
        elif command == 'get_stats':
            return {
                'total_score': state['total_score'],
                'active_combos': dict(state['combos']),
                'inventory': dict(state['inventory']),
                'event_count': len(state['events'])
            }
        elif command == 'reset':
            state['total_score'] = 0
            state['combos'].clear()
            state['inventory'].clear()
            state['events'].clear()
            return 'reset complete'
        return 'unknown command'

    return handler

def process_raw_gaming_data(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    handler = create_gaming_data_handler()
    for entry in data_list:
        cmd = entry.get('command')
        args = entry.get('args', [])
        if cmd:
            handler(cmd, *args)
    return handler('get_stats')

def calculate_win_probability(player_stats: Dict[str, float], opponent_stats: Dict[str, float]) -> float:
    if not player_stats or not opponent_stats:
        return 0.5
    ratios = []
    for key in set(player_stats.keys()) & set(opponent_stats.keys()):
        if opponent_stats.get(key, 0) > 0:
            ratios.append(player_stats[key] / opponent_stats[key])
    if not ratios:
        return 0.5
    product = 1.0
    for r in ratios:
        product *= r
    geo_mean = product ** (1 / len(ratios))
    prob = 1 / (1 + (1 / geo_mean))
    return min(max(prob, 0.0), 1.0)