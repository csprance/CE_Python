# spaces objects evenly along a given axis
import sys

import better_cry as bc


def space(items, axis=int(sys.argv[1])):
    next_pos = items[0].position[axis]
    for item in items:
        measurement = [item.depth, item.width, item.height]
        new_position = item.position
        new_position[axis] = next_pos + measurement[axis]
        # # set the position of the brush
        item.position = new_position
        next_pos = next_pos + measurement[axis]


def main():
    level = bc.Level()
    space(level.selected)


if __name__ == "__main__":
    main()
