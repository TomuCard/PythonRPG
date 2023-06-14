import json
from Classes.Player import Player

def load(save_number):
    with open(f'Data/Saves/Save_{save_number}/map_data.json', 'r') as f:
        positional_datas = json.loads(f.read())
    with open(f'Data/Saves/Save_{save_number}/player_data.json', 'r') as f:
        player_data = json.loads(f.read())
    loaded_data = positional_datas
    saved_player = Player(player_data["name"], player_data["max_hp"], player_data["max_mana"], player_data["attacks"], player_data["magics"], player_data["equipped_items"], player_data["inventory"], player_data["statistics"])
    loaded_data["player"] = saved_player

    return loaded_data


