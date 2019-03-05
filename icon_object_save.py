import general
import lodtools
from icon_object_db import IconObjectDB
from user_values import UserValues


def save(name=False, overwrite=False, embellishment=None):
    """
	Save an Icon Setup
	:return: string name of the entity class name
	"""
    # name of icon_object in icon_level.cry
    ico_obj = "icon_object_shot"
    store = UserValues()

    # the obj to insert
    obj = dict()

    # instantiate our iodb
    try:
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return None

    # clear the selection
    general.clear_selection()

    # get the info from the icon_object_shot
    obj["pos"] = general.get_position(ico_obj)
    obj["scale"] = general.get_scale(ico_obj)
    obj["rot"] = general.get_rotation(ico_obj)
    obj["mtl"] = general.get_assigned_material(ico_obj)
    obj["tod"] = general.get_cvar("e_timeOfDay")

    # get the brush by selecting the ico_obj
    general.select_object(ico_obj)
    obj["brush"] = lodtools.getselected().lower()
    general.clear_selection()
    stored = io.get_obj_by_brush_and_mtl(obj["brush"], obj["mtl"])

    if embellishment:
        print("Saving Embellishments")
        obj["embellishment_48"] = embellishment["embellishment_48"]
        obj["embellishment_200"] = embellishment["embellishment_200"]
        obj["embellishment_2048"] = embellishment["embellishment_2048"]
        if "embellishment_under" in embellishment.keys():
            obj["embellishment_under"] = True
    else:
        icon_obj = store.get("current_icon_object")
        if icon_obj:
            keys = icon_obj.keys()
            if "embellishment_under" in keys:
                obj["embellishment_under"] = True
            if "embellishment_48" in keys:
                obj["embellishment_48"] = icon_obj["embellishment_48"]
            if "embellishment_200" in keys:
                obj["embellishment_200"] = icon_obj["embellishment_200"]
            if "embellishment_2048" in keys:
                obj["embellishment_2048"] = icon_obj["embellishment_2048"]

    if name:
        obj["name"] = name
    elif stored:
        obj["name"] = stored["name"]
        if not general.message_box_yes_no(str("Save " + stored["name"] + "?")):
            obj["name"] = general.edit_box("Entity ClassName")
        else:
            overwrite = True
    else:
        obj["name"] = general.edit_box("Entity ClassName")

    if io.insert_object(obj) is False:
        if overwrite:
            io.insert_object(obj, override=True)
        else:
            if general.message_box_yes_no("Overwrite?"):
                io.insert_object(obj, override=True)
    print("Storing Item into UserValues")
    store.set("current_icon_object", obj)
    return obj["name"]


if __name__ == "__main__":
    save()
