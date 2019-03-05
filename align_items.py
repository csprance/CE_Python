import sys

import general


def align_x(selected_items):
    item_positions = [general.get_position(item) for item in selected_items]
    max_x = max([item[0] for item in item_positions])
    for idx, item in enumerate(selected_items):
        general.set_position(
            item, max_x, item_positions[idx][1], item_positions[idx][2]
        )


def align_y(selected_items):
    item_positions = [general.get_position(item) for item in selected_items]
    max_y = max([item[1] for item in item_positions])
    for idx, item in enumerate(selected_items):
        general.set_position(
            item, item_positions[idx][0], max_y, item_positions[idx][2]
        )


def align_z(selected_items):
    item_positions = [general.get_position(item) for item in selected_items]
    max_z = max([item[2] for item in item_positions])
    for idx, item in enumerate(selected_items):
        general.set_position(
            item, item_positions[idx][0], item_positions[idx][1], max_z
        )


def align_min_x(selected_items):
    item_positions = [general.get_position(item) for item in selected_items]
    min_x = min([item[0] for item in item_positions])
    for idx, item in enumerate(selected_items):
        general.set_position(
            item, min_x, item_positions[idx][1], item_positions[idx][2]
        )


def align_min_y(selected_items):
    item_positions = [general.get_position(item) for item in selected_items]
    min_y = min([item[1] for item in item_positions])
    for idx, item in enumerate(selected_items):
        general.set_position(
            item, item_positions[idx][0], min_y, item_positions[idx][2]
        )


def align_min_z(selected_items):
    item_positions = [general.get_position(item) for item in selected_items]
    min_z = min([item[2] for item in item_positions])
    for idx, item in enumerate(selected_items):
        general.set_position(
            item, item_positions[idx][0], item_positions[idx][1], min_z
        )


if __name__ == "__main__":
    _selected_items = general.get_names_of_selected_objects()
    x = True if sys.argv[1] == "x" else False
    y = True if sys.argv[1] == "y" else False
    z = True if sys.argv[1] == "z" else False
    neg_x = True if sys.argv[1] == "-x" else False
    neg_y = True if sys.argv[1] == "-y" else False
    neg_z = True if sys.argv[1] == "-z" else False
    if x:
        align_x(_selected_items)
    if y:
        align_y(_selected_items)
    if z:
        align_z(_selected_items)
    if neg_x:
        align_min_x(_selected_items)
    if neg_y:
        align_min_y(_selected_items)
    if neg_z:
        align_min_z(_selected_items)
