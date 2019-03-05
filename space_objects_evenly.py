# spaces objects evenly along a given axis
import sys

import general
import better_cry as bc


def get_axis():
    return int(sys.argv[1])


def space(items, spacing=1.0, axis=get_axis()):
    initial_pos = items[0].position
    for idx, brush in enumerate(items):
        # get our brush
        new_position = brush.position
        new_position[axis] = initial_pos[axis] + (spacing * idx)
        # set the position of the brush
        brush.position = new_position


def main():
    level = bc.Level()
    space_between = float(general.edit_box("Space between"))
    space(level.selected, space_between)


if __name__ == "__main__":
    main()
