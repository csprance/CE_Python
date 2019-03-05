from better_cry import Level


def unrotate():
    level = Level()
    for item in level.selected:
        item.rotation = (0, 0, 0)


if __name__ == "__main__":
    unrotate()
