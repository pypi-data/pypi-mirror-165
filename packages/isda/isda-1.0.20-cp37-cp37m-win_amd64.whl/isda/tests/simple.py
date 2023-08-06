given_value_list = [2]
given_value_offset = [-0.46]

attach_list = [1, 5, 8]
attach_list_amend = [3., 6., 9.]

print(attach_list, attach_list_amend)


def myfunc(given_value_list, given_value_offset, attach_list, attach_list_amend):
    for given_value, give_offset in zip(given_value_list, given_value_offset):
        print(f"{given_value} {give_offset}")
        closest_value = min(attach_list, key=lambda list_value: abs(list_value - given_value))
        nearest_given_index = attach_list.index(closest_value)
        print(f"closest_value {closest_value} nearest_given_index{nearest_given_index}")
        attach_list_amend[nearest_given_index] += give_offset


myfunc(given_value_list, given_value_offset, attach_list, attach_list_amend)

print(attach_list, attach_list_amend)
