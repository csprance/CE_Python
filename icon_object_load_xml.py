# coding:utf-8
import general
import cry_utils
from icon_object_load import add_to_scene, get_default_object
from icon_object_db import IconObjectDB
from icon_object_save import save
from cry_utils import (
    is_skin,
    is_vehicle_skin,
    get_base_item_xml_path,
    get_item_material_from_skin_xml,
    get_item_name_from_xml,
    get_item_geometry_from_xml,
    get_item_material_from_xml,
    get_vehicle_name_from_skin,
    get_skin_name,
)


def load_by_xml():
    try:
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return False
    xml_filepath = general.open_file_box()
    if not xml_filepath:
        return False
    entity_name = get_item_name_from_xml(xml_filepath)
    obj = io.get_obj_by_name(entity_name)

    if is_vehicle_skin(xml_filepath):
        vehicle_skin_name = get_skin_name(xml_filepath)
        base_item_name = get_vehicle_name_from_skin(xml_filepath)
        io_obj = (
            io.get_obj_by_name(vehicle_skin_name)
            if io.get_obj_by_name(vehicle_skin_name) is not None
            else io.get_obj_by_name(base_item_name)
        )
        tod = "12"
        if "tod" in io_obj:
            tod = io_obj["tod"]
        add_to_scene(
            get_default_object(
                io_obj["brush"],
                mtl=get_item_material_from_skin_xml(xml_filepath),
                name=vehicle_skin_name,
                pos=io_obj["pos"],
                rot=io_obj["rot"],
                scale=io_obj["scale"],
                tod=tod,
            )
        )
        return True

    # check if it's a skin file if it is grab the base item xml file and use that.
    if is_skin(xml_filepath):
        base_item_xml_path = get_base_item_xml_path(xml_filepath)
        base_item_name = get_item_name_from_xml(base_item_xml_path)
        io_obj = io.get_obj_by_name(base_item_name)
        tod = "12"
        if "tod" in io_obj:
            tod = io_obj["tod"]
        add_to_scene(
            get_default_object(
                io_obj["brush"],
                mtl=get_item_material_from_skin_xml(xml_filepath),
                name=entity_name,
                pos=io_obj["pos"],
                rot=io_obj["rot"],
                scale=io_obj["scale"],
                tod=tod,
            )
        )
        return True

        # if the object already exists grab it and add it to the scene
    if obj is not None:
        add_to_scene(obj)
        return True

    # add the object to the scene
    add_to_scene(
        get_default_object(
            get_item_geometry_from_xml(xml_filepath),
            mtl=get_item_material_from_xml(xml_filepath),
            name=entity_name,
        )
    )
    save(entity_name)
    return True


if __name__ == "__main__":
    # reload(cry_utils)
    load_by_xml()
