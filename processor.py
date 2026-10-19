import logging

def sanitize_input(user_data):
    """Cleans raw controller input bytes for game logic."""
    if not isinstance(user_data, dict):
        return None
    
    cleaned = {}
    for key, val in user_data.items():
        # Force coordinate inputs into gaming-safe bounds
        if key in ['x', 'y']:
            cleaned[key] = max(0, min(1920, int(val)))
        elif isinstance(val, str):
            cleaned[key] = val[:16].strip()
        else:
            cleaned[key] = val
    return cleaned

def run_game_loop(queue):
    """Main processing loop with unorthodox input validation."""
    while True:
        try:
            raw_input = queue.get()
            if raw_input is None:
                break
            
            validated = sanitize_input(raw_input)
            if validated:
                # Dispatch validated signal to physics engine
                print(f"Processing move: {validated}")
            else:
                logging.warning("Dropping malformed input frame")
        except Exception as e:
            logging.error(f"Input stream corruption: {e}")

if __name__ == "__main__":
    # Demo processing with a dummy queue
    import queue
    q = queue.Queue()
    q.put({'x': 500, 'y': 'invalid', 'cmd': 'jump  '})
    q.put(None)
    run_game_loop(q)