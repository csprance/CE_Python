# loads an icon object one at a time from the icon object db and keeps track of which ones have already been loaded
import general
from icon_object_db import IconObjectDB
from cry_utils import (
    get_item_geometry_from_xml,
    get_item_material_from_xml,
    get_item_name_from_xml,
)
from icon_object_load import get_default_object, add_to_scene
from icon_object_save import save
from user_values import UserValues
from test import items


def add_item_to_processed_list(name, _store):
    todo = _store.get("todo")
    done = _store.get("done")
    done.append(name)
    _store.set("done", done)
    _store.set("todo", filter(lambda x: x != name, todo))


def load_batch(_store):
    try:
        io = IconObjectDB()
    except ValueError as val_err:
        general.message_box_ok(str(val_err))
        return False
    xml_path = store.get("todo")[0]
    name = get_item_name_from_xml(xml_path)
    if xml_path is not None:
        icon_object = io.get_obj_by_name(name)
        if icon_object:
            add_to_scene(icon_object)
        else:
            print('Inserting ' + name + 'to icon database')
            add_to_scene(
                get_default_object(
                    get_item_geometry_from_xml(xml_path),
                    mtl=get_item_material_from_xml(xml_path),
                    name=name
                )
            )
            save(name)
        add_item_to_processed_list(xml_path, store)


if __name__ == "__main__":
    store = UserValues()
    if store.get("todo") is None:
        store.set("todo", items)
        store.set("done", [])
    load_batch(store)
