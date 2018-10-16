

def settings(place):
    threshold_dict = None
    target_list = None
    time_to_kill = None
    move_another_area = None
    target_img_path = None
    area_dict = None
    x_max, x_min, y_max, y_min = (0, 29, 0, 14)
    transition_time = list()
    transition = list()

    if place == "sea":
        threshold_dict = {"Berger": 0.9, "Preta": 0.8, "Mermaid": 0.9}
        target_list = ["Berger", "Preta", "Mermaid"]   # ordered by priority, left is higher than right
        time_to_kill = 3
        move_another_area = True
        area_dict = {"area1": (11, 0), "area2": (9, 13), "next_area": "2"}
        target_img_path = "data/target/sea"
    elif place == "magma":
        target_list = ["Item", "Berger", "Zombie", "YellowPreta"]   # ordered by priority, left is higher than right
        threshold_dict = {"Berger": 0.9, "YellowPreta": 0.85, "Zombie": 0.82, "Item": 0.86}
        time_to_kill = 5
        move_another_area = True
        area_dict = {"area1": (15, 0), "area2": (15, 13), "next_area": "1"}
        target_img_path = "data/target/magma"
        x_min, x_max = (0, 29)
        y_min, y_max = (0, 14)
        transition_time = [3, 4, 4, 3, 6, 7, 7, 7, 3, 4, 4, 6]
        transition = [(21, 13), (23, 13), (25, 13), (29, 8), (23, 13), (0, 13), (6, 13), (29, 10), (7, 13), (9, 11),
                      (5, 13), (27, 11)]
    elif place == "forest":
        threshold_dict = {"Berger": 0.9, "Wolf": 0.90, "Me": 0.9, "MyHead": 0.80}
        target_list = ["Wolf", "Berger", "Me", "MyHead"]  # ordered by priority, left is higher than right
        time_to_kill = 8
        move_another_area = False
        target_img_path = "data/target/forest"
    elif place == "iceCastle":
        threshold_dict = {"Berger": 0.9, "Iceg": 0.90, "Me": 0.9, "Item": 0.87}
        target_list = ["Item", "Iceg", "Berger", "Me"]  # ordered by priority, left is higher than right
        time_to_kill = 11
        move_another_area = False
        target_img_path = "data/target/iceCastle"
        x_min, x_max = (6, 23)
        y_min, y_max = (1, 13)
        transition = [(15, 0), (14, 5), (14, 0), (14, 4), (14, 0), (14, 2), (14, 0), (14, 0), (14, 0)]
        transition_time = [3, 3, 4, 2, 3, 3, 3, 3, 5]
    elif place == "basement":
        threshold_dict = {"Berger": 0.9, "Flaredeathknight": 0.90, "Me": 0.9, "Kaonashi": 0.80, "Item": 0.88}
        target_list = ["Kaonashi", "Flaredeathknight", "Item", "Berger", "Me"]  # ordered by priority, left is higher than right
        time_to_kill = 18
        move_another_area = False
        target_img_path = "data/target/basement"
        x_min, x_max = (4, 24)
        y_min, y_max = (4, 13)

    info_dict = {"threshold_dict": threshold_dict, "target_list": target_list, "time_to_kill": time_to_kill,
                "move_another_area": move_another_area, "target_img_path": target_img_path, "area_dict": area_dict,
                "range": (x_min, x_max, y_min, y_max), "transition": transition, "transition_time": transition_time}

    return info_dict