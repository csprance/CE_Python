import general
from icon_object_load import load, add_to_scene
from icon_object_db import IconObjectDB


def load_by_name():
    try:
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return False
    name = general.edit_box("Entity Classname")
    if not name:
        return False
    obj = io.get_obj_by_name(name)
    print(obj)
    if obj is not None:
        add_to_scene(obj)
    if obj is None:
        if general.message_box_yes_no("Does not Exist! \n Load By Brush?"):
            # load it by brush
            load()


if __name__ == "__main__":
    load_by_name()
