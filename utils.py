import json
import re

def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a dictionary.')