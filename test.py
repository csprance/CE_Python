import better_cry as bc

if __name__ == "__main__":
    reload(bc)
    level = bc.Level()
    for item in level.selected:
        item.position = [item.position[0] + 1, item.position[1] + 1, item.position[2] + 1]
    # print(level.objects)
