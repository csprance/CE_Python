from random import randint
import better_cry as bc


def rotate_randomly():
    level = bc.Level()
    for item in level.selected:
        [x, y, z] = (randint(0, 360), randint(0, 360), randint(0, 360))
        print("Rotating Object: %s (%s, %s, %s)" % (item, x, y, z))
        item.rotation = (x, y, z)


if __name__ == "__main__":
    rotate_randomly()
