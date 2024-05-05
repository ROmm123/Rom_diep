import json

def main():
    # Truncated data string
    data_str = '[{"ID": 0, "rect_center_x": 410.63070275842665, "rect_center_y": 256.2737131823204, "rect_width": 25, "rect_height": 25, "tangent_x": 407.08713517228443, "player_position_x": 12000, "player_position_y": 0, "player_radius": 30, "weapon_angle": -1.3323040591849085, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}][{"ID": 0, "rect_center_x": 410.63070275842665, "rect_center_y": 256.2737131823204, "rect_width": 25, "rect_height": 25, "tangent_x": 407.08713517228443, "player_position_x": 12000, "player_position_y": 0, "player_color": [255, 0, 0], "player_radius": 30, "weapon_angle": -1.3323040591849085, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}][{"ID": 0, "rect_center_x": 410.63070275842665, "rect_center_y": 256.2737131823204, "rect_width": 25, "rect_height": 25, "tangent_x": 407.08713517228443, "player_position_x": 12000, "player_position_y": 0, "player_color": [255, 0, 0], "player_radius": 30, "weapon_angle": -1.3323040591849085, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}][{"ID": 0, "rect_center_x": 410.63070275842665, "rect_center_y": 256.2737131823204, "rect_width": 25, "rect_height": 25, "tangent_x": 407.08713517228443, "player_position_x": 12000, "player_position_y": 0, "player_color": [255, 0, 0], "player_radius": 30, "weapon_angle": -1.3323040591849085, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}][{"ID": 0, "rect_center_x": 410.63070275842665, "rect_center_y": 256.2737131823204, "rect_width": 25, "rect_height": 25, "tangent_x": 407.08713517228443, "player_position_x": 12000, "player_position_y": 0, "player_color": [255, 0, 0], "player_radius": 30, "weapon_angle": -1.3323040591849085, "shot_velocity_x": 0, "shot_velocity_y": 0, "shot_start_x": 0, "shot_start_y": 0, "damage dealt": 0}][{"ID": 0, "rect_center_x": 410.63070275842665, "rect_center_y": 256.273713182'
    print("data str , in network : " + data_str)
    if data_str[0] == '[':
        index = data_str.find(']')
        index1 = index
        while str(data_str[index1 - 1]).isdigit():  # }]
            # if isinstance(int(data_str[index - 1]), int):
            index1 = data_str[index1+1:].find(']') # [[12345 , 243633] 353535}]
            index1 += index +1
            print(data_str[index1 - 1])
            index = index1
        # Remove the truncated part
        data_str = data_str[:index1 + 1]
        print("data str , after modification : " + str(data_str))

        # Split the concatenated JSON string into individual JSON objects
        json_list = []
        start = 1
        while start < len(data_str) - 2:
            end = data_str.find('}', start)
            json_list.append(data_str[start:end + 1])
            start = end
        # Parse each JSON object and add it to the list
        data_list = []
        print("json list , before loading the elements : "+str(json_list))
        for json_str in json_list:
            print(type(json_str))
            print("the element in the unloaded list : "+str(json_str))
            data_list.append(json.loads(json_str))

        # Print the resulting list
        print("updated dict list : "+str(data_list))

        return data_list

if __name__ == '__main__':
    main()
