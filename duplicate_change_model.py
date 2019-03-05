import json
from icon_object_db import IconObjectDB


def replace_plated_with_wood(item):
    wooden_item = item
    wooden_item["name"] = item["name"].replace("plated", "wood")
    wooden_item["brush"] = item["brush"].replace("plated", "wood")
    wooden_item["mtl"] = item["mtl"].replace("plated", "wood")
    return wooden_item


def duplicate_change_model():
    io = IconObjectDB()
    with open("D:\perforce\dev\EI\icons\icon_objects.json") as icon_object_json_file:
        json_db = json.loads("".join(icon_object_json_file.readlines()))["_default"]
        db_items = [json_db[key] for key in json_db.keys()]
        plated_items = filter(
            lambda x: x["brush"].startswith("objects/basebuilding/plated/"), db_items
        )
        wooden_items = map(lambda x: replace_plated_with_wood(x), plated_items)
        inserted = [io.insert_object(obj) for obj in wooden_items]
        print(inserted)


if __name__ == "__main__":
    duplicate_change_model()
