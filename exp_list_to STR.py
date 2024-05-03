import json

def main():
    # Truncated data string
    data_str = '[{"ID": 0, "rect_center_x": 443.7472259610955, "rect_center_y": 310.54420318036665, "rect_width": 25, "rect_height": 25, "tangent_x": 429.164817307397, "player_position_x": 12000, "player_position_y": 0, "player_color": [255, 0, 0], "player_radius": 30, "weapon_angle": 0.23651453636043474, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}]'

    # Check if data_str is truncated
    index = data_str.find(']')
    if index != -1:
        # Remove the truncated part
        data_str = data_str[:index + 1]

    # Split the concatenated JSON string into individual JSON objects
    json_list = []
    start = 0
    while start < len(data_str):
        end = data_str.find('}', start) + 1
        json_list.append(data_str[start:end])
        start = end

    # Parse each JSON object and add it to the list
    data_list = []
    for json_str in json_list:
        data_list.append(json.loads(json_str))

    # Print the resulting list
    print(data_list)

if __name__ == '__main__':
    main()
