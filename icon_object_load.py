import general
import material
from cry_utils import norm_path_for_ce
from take_screenshot import take_screenshot
from user_values import UserValues
from icon_object_db import IconObjectDB
from tools_shelf_actions import cycleConsolValue


def get_default_object(
    brush, mtl=None, name="Default", pos=None, rot=None, scale=None, tod=None
):
    if scale is None:
        scale = [1, 1, 1]
    if rot is None:
        rot = [0, 0, 0]
    if pos is None:
        pos = [996.4752, 1057.014, 62.3948]
    if tod is None:
        tod = "14.3"
    return {
        "scale": scale,
        "name": name,
        "pos": pos,
        "brush": brush,
        "mtl": mtl,
        "rot": rot,
        "tod": tod,
    }


def init_screenshot_values():
    """
    This runs once on user_values init function created by the add to scene function which should be run every time
    an item is added to the scene so the screenshot bug never happens
    :return: None
    """
    general.set_cvar("r_DisplayInfo", 0)
    general.set_cvar("r_AntiAliasingMode", 3)
    general.set_cvar("r_CustomResWidth", 3840)
    general.set_cvar("r_CustomResHeight", 2160)
    take_screenshot(open_folder=False)
    return None


def add_to_scene(obj):
    print("Adding: " + obj["name"])
    store = UserValues(init_funcs=[init_screenshot_values])
    store.set("current_icon_object", obj)
    ico_obj = "icon_object_shot"
    ico_obj_2 = "icon_object_shot_2"
    # update our ico_obj based on the settings from the collected icon_object
    general.set_position(ico_obj, obj["pos"][0], obj["pos"][1], obj["pos"][2])
    general.set_scale(ico_obj, obj["scale"][0], obj["scale"][1], obj["scale"][2])
    general.set_rotation(ico_obj, obj["rot"][0], obj["rot"][1], obj["rot"][2])
    general.set_entity_geometry_file(ico_obj, str(obj["brush"]))
    general.select_object(ico_obj)
    material.reset_selection()
    if obj["mtl"] is not None:
        general.set_custom_material(ico_obj, str(obj["mtl"]))
    if "tod" in obj.keys():
        tod_list = [str("e_TimeOfDay %s" % obj["tod"])]
        cycleConsolValue("mode_%s" % "e_TimeOfDay", tod_list)
    # if "brush_secondary" in obj.keys():
    #     # update our ico_obj based on the settings from the collected icon_object
    #     general.set_position(
    #         ico_obj_2, obj["pos_2"][0], obj["pos_2"][1], obj["pos_2"][2]
    #     )
    #     general.set_scale(
    #         ico_obj_2, obj["scale_2"][0], obj["scale_2"][1], obj["scale_2"][2]
    #     )
    #     general.set_rotation(
    #         ico_obj_2, obj["rot_2"][0], obj["rot_2"][1], obj["rot_2"][2]
    #     )
    #     general.set_entity_geometry_file(ico_obj_2, str(obj["brush_2"]))
    #     general.select_object(ico_obj_2)
    #     material.reset_selection()
    #     if obj["mtl_2"] is not None:
    #         general.set_custom_material(ico_obj_2, str(obj["mtl_2"]))
    # else:
    #     general.set_position(ico_obj_2, 0, 0, 0)


def load():
    try:
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return False
    brush = norm_path_for_ce(general.open_file_box(), maintain_casing=False)
    obj = io.get_obj_by_brush(brush)
    if obj is not None:
        add_to_scene(obj)
    else:
        add_to_scene(get_default_object(brush))


if __name__ == "__main__":
    load()
