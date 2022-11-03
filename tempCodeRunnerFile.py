in_point_item_adress_details_ending = item_adress_details[::-1].index(",")
                in_point_item_adress_details_ending2 = item_adress_details[::-1].index(" ")
                item_minutes_for_subway = item_adress_details[len(item_adress_details) - in_point_item_adress_details_ending + 1 : len(item_adress_details) - 1]
                in_point_item_minutes_for_subway = item_minutes_for_subway.index(" ")
                item_minutes_for_subway = int(item_minutes_for_subway[: in_point_item_minutes_for_subway])