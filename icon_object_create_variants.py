# will take the currently selected object and add variants from xml files
import general
from icon_object_db import IconObjectDB
from better_file_dialog.editor_run import get_file_path_list
from cry_utils import (
    get_items_dir,
    get_item_material_from_xml,
    get_item_geometry_from_xml,
    get_item_name_from_xml,
)


def overwrite_values(original, new):
    return {
        "scale": original["scale"],
        "pos": original["pos"],
        "rot": original["rot"],
        "name": new["name"],
        "brush": new["brush"],
        "mtl": new["mtl"],
    }


def create_variants():
    try:
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return None
    general.clear_selection()
    general.select_object("icon_object_shot")
    # get the other items name mtl and brush
    item_filepaths = get_file_path_list(".xml", get_items_dir())
    # overwrite the name mtl and brush
    icon_object_variants = [
        {
            "name": get_item_name_from_xml(filepath),
            "brush": get_item_geometry_from_xml(filepath),
            "mtl": get_item_material_from_xml(filepath),
            "scale": general.get_scale("icon_object_shot"),
            "pos": general.get_position("icon_object_shot"),
            "rot": general.get_rotation("icon_object_shot"),
        }
        for filepath in item_filepaths
    ]
    # save it
    for icon_obj in icon_object_variants:
        io.insert_object(icon_obj, override=True)


if __name__ == "__main__":
    create_variants()
