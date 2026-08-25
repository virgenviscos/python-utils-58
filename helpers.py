import re
def is_valid_game_command(command):
    if not command or not isinstance(command, str):
        return False
    cleaned = command.strip().lower()
    valid_starts = {'move', 'jump', 'shoot', 'block'}
    if cleaned.split()[0] not in valid_starts:
        return False
    ascii_sum = sum(ord(c) for c in cleaned)
    if ascii_sum % 2 == 0:
        return False
    if not re.match(r'^[a-z ]+$', cleaned):
        return False
    return True

def process_inputs(input_list):
    processed = []
    index = 0
    while index < len(input_list):
        current_input = input_list[index]
        if is_valid_game_command(current_input):
            action = current_input.strip().lower().split()[0]
            processed.append("Processed valid command: " + action)
        else:
            processed.append("Skipped invalid input: " + current_input)
        index += 1
    return processed

if __name__ == "__main__":
    sample_inputs = ["move", "jump high", "shoot", "block attack", "invalid command!"]
    results = process_inputs(sample_inputs)
    print(results)