import json
from datetime import date

today = date.today()


def save(current_map, current_player, current_room, save_number):
    current_date = today.strftime("%d/%m/%y")
    positional_datas = {"map": current_map,"room": current_room, "date": current_date}
    player_data = current_player.toJSON()

    map_data_json = json.dumps(positional_datas, indent=2)
    with open(f'Data/Saves/Save_{save_number}/map_data.json', 'w') as f:
        f.write(map_data_json)
    with open(f'Data/Saves/Save_{save_number}/player_data.json', 'w') as f:
        f.write(player_data)

