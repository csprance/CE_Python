import fnmatch
import os
import re
import general


def get_all_damn_cgfs(folder, file_type="cgf"):
    """gets all the cgfs files from a self.folder recursively"""
    items = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, file_type):
            items.append(os.path.join(root, filename))
    return items


def get_dws_models():
    cgfs = get_all_damn_cgfs("D:\perforce\dev\GameSDK\Objects", "*.cgf")
    dws_items_re = re.compile(r"dws_.*")
    return filter(lambda x: dws_items_re.search(x), cgfs)


def set_increment_amount():
    x1, y1, z1, x2, y2, z2 = general.get_selection_aabb()
    # width of x + 1/2 width of x because it measures from center point
    increment_amount = (x2 - x1) + ((x2 - x1) * 0.5)
    general.clear_selection()
    return increment_amount


def norm_path_for_ce(path):
    split_path = os.path.normpath(path).split(os.path.sep)
    for idx, part in enumerate(split_path):
        if part == "GameSDK":
            return "/".join(split_path[idx + 1 :])


def add_cgfs(items):
    """spawn in each of our items from self.item_names and then select them"""
    num_cols = 25
    x = 0
    increment_amount = 0
    for idx, item in enumerate(items):
        if idx % num_cols == 0:
            # increment by some amount set by the last objects x width
            x += increment_amount
        general.select_object(
            general.new_object(
                "Brush", norm_path_for_ce(item), "", x, (idx % num_cols) * 55, 32
            )
        )
        increment_amount = set_increment_amount()
    print(
        "Added %s CGF Files to the map. Thanks for adding every damn CGF!" % len(items)
    )


if __name__ == "__main__":
    add_cgfs(get_dws_models())
