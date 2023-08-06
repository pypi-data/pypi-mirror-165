import json
from pathlib import Path

def load_soup_bowl():
    with open(Path(Path(__file__).parent/'bowl.json'), 'r+') as file:
        try:
            bowl = json.load(file)
        except json.JSONDecodeError as e:
            bowl = {}

    return bowl

def dump_soup_bowl(soup: dict):
    with open(Path(Path(__file__).parent/'bowl.json'), 'w+') as file:
        file.write(json.dumps(soup))
    
    return

def clean_soup_bowl():
    with open(Path(Path(__file__).parent/'bowl.json'), 'w+') as file:
        file.write(json.dumps({}))
    
    return