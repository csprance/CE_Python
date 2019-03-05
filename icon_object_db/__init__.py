import os
import sys

sys.path.append(os.path.dirname(__file__))
from tinydb import TinyDB, Query, where


class IconObjectDB(object):
    """The Class for inserting objects in the icon_object.json db using tinydb"""

    def __init__(self):
        super(IconObjectDB, self).__init__()
        try:
            self.db = TinyDB(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "..",
                        "..",
                        "EI",
                        "icons",
                        "icon_objects.json",
                    )
                )
            )
        except Exception as err:
            raise ValueError("Database is locked")

    def insert_object(self, obj, override=False):
        if not self.db.contains(where("name") == obj["name"]):
            print("Inserting: " + str(obj['name']))
            self.db.insert(obj)
        else:
            if self.warn_user(override):
                print("Overwriting: " + str(obj['name']))
                self.db.update(obj, where("name") == obj["name"])
            else:
                return False

    def get_values(self, value):
        obj_list = list()
        for obj in self.get_all():
            if value in obj:
                obj_list.append(obj[value])
        return obj_list

    def get_obj_by_mtl(self, mtl):
        if self.db.contains(where("mtl") == str(mtl)):
            return self.db.search(where("mtl") == str(mtl))[0]

    def get_obj_by_brush(self, brush):
        if self.db.contains(where("brush") == str(brush)):
            return self.db.search(where("brush") == str(brush))[0]

    def get_obj_by_brush_and_mtl(self, brush, mtl):
        if self.db.contains(
            (where("brush") == str(brush)) & (where("mtl") == str(mtl))
        ):
            return self.db.search(
                (where("brush") == str(brush)) & (where("mtl") == str(mtl))
            )[0]

    def get_objs_by_brush(self, brush):
        if self.db.contains(where("brush") == str(brush)):
            return self.db.search(where("brush") == str(brush))

    def get_obj_by_name(self, name):
        if self.db.contains(where("name") == name):
            return self.db.search(where("name") == name)[0]

    def get_all(self):
        return self.db.search(lambda x: True)

    @staticmethod
    def warn_user(override):
        return override
