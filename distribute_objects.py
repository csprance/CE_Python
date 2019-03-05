# distributes a selection of objects along a given access
import sys
import random
from better_cry import Level


def distribute(axes, distance):
    level = Level()
    for item in level.selected:
        for axis in axes:
            new_position = item.position
            new_position[axis] = item.position[axis] + random.uniform(-distance, distance)
            item.position = new_position
        item.rotation = (item.rotation[0], item.rotation[1], item.rotation[2] + random.uniform(0, 360))


if __name__ == "__main__":
    # User input value
    # max_distance = general.edit_box("Max Distribution Distance")
    max_distance = 0.32133
    switch = {
        "xy": lambda: distribute([0, 1], float(max_distance)),
        "xz": lambda: distribute([0, 2], float(max_distance)),
        "yz": lambda: distribute([1, 2], float(max_distance)),
    }
    switch[sys.argv[1]]()
