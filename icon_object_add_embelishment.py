from icon_object_db import IconObjectDB
from icon_object_capture import get_icon_object_in_scene
from user_values import UserValues


def add_embellishment():
    io = IconObjectDB()
    store = UserValues()
    obj = get_icon_object_in_scene()
    obj['embellishment_48'] = ''
    obj['embellishment_200'] = ''
    obj['embellishment_2048'] = ''
    save()


if __name__ == "__main__":
    add_embellishment()
