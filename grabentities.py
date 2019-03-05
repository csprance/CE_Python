#!/usr/bin/python
"""
Go through and place all entities from a folder into a scene
Chris Sprance
Entrada interactive
"""
import general
import os
import re
from better_file_dialog.editor_run import get_file_path_list


class EntityGrabber(object):
    """
    Grabs entities from a folder and places them in the sandbox editor
    This is because a lot of time you need to test a lot of items and dragging them by hand blows!
    On Script Activation it will Open a file dialog and ask you to choose a folder full of entities you would like to spawn
    These xml files will be scanned for there item names and that will be used to spawn items in a short distance
    from each other and then select them all so you can quickly shift click to place the lot of items
    """

    def __init__(self):
        super(EntityGrabber, self).__init__()
        general.clear_selection()
        self.folder = str()  # folder to get all item xml files from
        self.file_type = "*.xml"
        self.item_names = list()  # a list of ItemNames from xml files
        self.xml_files = ()  # a list of a xml file paths
        self.excluded_files = (
            self.get_excluded_files_list()
        )  # a list of all the entity names not to spawn
        self.items = list()

    def get_user_input(self):
        """calls the function that opens our file dialog and returns a filepath"""
        self.xml_files = get_file_path_list(
            ".xml", os.path.abspath(r"GameSDK\Scripts\Entities\Items\XML")
        )

    def get_names_from_xml(self):
        """gets all the  item names from self.xml_files"""
        for xml in self.xml_files:
            with open(xml, "r") as f:
                x = re.findall(r'"(.*?)"', f.readline())
                if len(x) > 0:
                    if x[0] not in self.excluded_files:
                        self.item_names.append(x[0])

    def add_entities(self):
        """spawn in each of our items from self.item_names and then select them"""
        num_cols = 25
        x = 0
        y = 0
        for idx, item in enumerate(self.item_names):
            if idx % num_cols == 0:
                x += 1
            self.items.append(
                general.new_object("Entity", item, "", x, idx % num_cols, 0)
            )
        # clear the selection and add the new items to the selection
        general.select_objects(self.items)

    @staticmethod
    def get_excluded_files_list():
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "excluded_entities.txt"
            ),
            "r",
        ) as f:
            return f.read().splitlines()

    def start(self):
        """main process to run after instantiating class"""
        # get the entities
        self.get_user_input()
        for xml in self.xml_files:
            print(xml)
        # get names from xmls
        self.get_names_from_xml()
        # add entities to map using names
        self.add_entities()


def main():
    eg = EntityGrabber()
    eg.start()


# run the program
if __name__ == "__main__":
    main()
