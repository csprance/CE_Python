# TODO - Add in embellishments and update for argparse changes
# takes the screenshot for an icon
import os
import sys
import subprocess

import general
import lodtools
from cry_utils.get_files_by_type import get_all_files
from user_values import UserValues
from icon_object_db import IconObjectDB
from icon_object_save import save


def execute_external_icon_exe(scripts_dir, name, images, embellishments=""):
    exe_path = os.path.join(scripts_dir, "dist", "icon_object_create_icon.exe")
    extra_args = " ".join(sys.argv[1:])
    _name = "--name " + name
    _images = "--images " + space_separator(images)
    command_string = "%s %s %s %s %s" % (
        exe_path,
        _name,
        extra_args,
        embellishments,
        _images,
    )
    subprocess.Popen(command_string)


def space_separator(arr):
    """
    Turns an array of string into a string with a space separator
    :param arr: str[]
    :return: str
    """
    x = ""
    for item in arr:
        x += " " + item + " "
    return x


def names_different(io_obj, store_obj):
    return io_obj["name"] != store_obj["name"]


def materials_same(io_obj, store_obj):
    return io_obj["mtl"] == store_obj["mtl"]


def brush_same(io_obj, store_obj):
    return io_obj["brush"] == store_obj["brush"]


def get_icon_object_in_scene():
    try:
        store = UserValues()
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return None
    store_obj = store.get("current_icon_object")
    if store_obj:
        print('Returning Stored Object from User Values')
        print(store_obj)
        return store_obj
    # if we can't find a stored version try and find it
    if not store_obj:
        general.select_object("icon_object_shot")
        obj = io.get_obj_by_brush_and_mtl(
            lodtools.getselected().lower(),
            general.get_assigned_material("icon_object_shot"),
        )
        if obj:
            return obj
    # object was not set in store and is not set in io_db
    return None


def capture():
    scripts_dir = os.path.abspath(os.path.dirname(__file__))
    screenshot_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "user", "screenshots")
    )
    images = get_all_files(".jpg", screenshot_dir)
    general.clear_selection()
    if general.is_helpers_shown():
        general.toggle_helpers()
    # if general.get_viewport_size() == (3840, 2160):
    #     general.set_viewport_size(3840, 2160)
    if len(sys.argv) == 3:
        if sys.argv[2] == "--pink":
            general.set_position("icon_pink_screen", 992.4509, 1047.51, 47.6817)
            general.set_position("icon_green_screen", 0, 0, 0)
    else:
        general.set_position("icon_green_screen", 992.4509, 1047.51, 47.6817)
        general.set_position("icon_pink_screen", 0, 0, 0)
    general.run_console("r_getScreenshot 1")
    obj = get_icon_object_in_scene()
    keys = obj.keys()
    embellishment_string = ""
    if u"embellishment_48" in keys:
        embellishment_string += "--embellishment_48 " + obj["embellishment_48"] + " "
    if u"embellishment_200" in keys:
        embellishment_string += "--embellishment_200 " + obj["embellishment_200"] + " "
    if u"embellishment_2048" in keys:
        embellishment_string += "--embellishment_2048 " + obj["embellishment_2048"] + " "
    if u"embellishment_under" in keys:
        embellishment_string += "--embellishment_under"
    print(embellishment_string)
    if obj:
        # the object exists in our db
        # save it and overwrite the current version then execute_external_icon_exe the script
        execute_external_icon_exe(
            scripts_dir,
            save(obj["name"], overwrite=True),
            images,
            embellishments=embellishment_string,
        )
    else:
        # the objects does not exist in our db
        # Ask the user what it is and save it and then execute_external_icon_exe the script
        execute_external_icon_exe(
            scripts_dir, save(), images, embellishments=embellishment_string
        )


if __name__ == "__main__":
    capture()
