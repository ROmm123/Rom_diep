import json

def main():
    # Truncated data string
    data_str = '[{"ID": 0, "rect_center_x": 443.84075221810446, "rect_center_y": 310.1483222727094, "rect_width": 25, "rect_height": 25, "tangent_x": 429.22716814540297, "player_position_x": 12000, "player_position_y": 0, "player_color": [255, 0, 0], "player_radius": 30, "weapon_angle": 0.22747498047282771, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}]'

    # Check if data_str is truncated
    index = data_str.find(']')
    if isinstance(int(data_str[index-1]) , int):
        index1 = data_str[index+2 :].find(']')
    index1+=index
        # Remove the truncated part
    data_str = data_str[:index1 + 3]

    # Split the concatenated JSON string into individual JSON objects
    json_list = []
    start = 1
    while start < len(data_str)-2:
        end = data_str.find('}', start)
        json_list.append(data_str[start:end+1])
        start = end

    # Parse each JSON object and add it to the list
    data_list = []
    for json_str in json_list:
        data_list.append(json.loads(json_str))

    # Print the resulting list
    print(data_list)
    print(type(data_list))

if __name__ == '__main__':
    main()
