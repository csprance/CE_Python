#!/usr/bin/python
"""
Go through and place all entities from a folder into a scene
Chris Sprance
Entrada interactive
"""

# glob looks through files in a smart way
import general
import fnmatch
import os
from BeautifulSoup import BeautifulSoup as BS


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
        # general.clear_selection()
        self.folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "GameSDK",
                "Scripts",
                "Entities",
                "Items",
                "XML",
            )
        )
        print(self.folder)
        self.file_type = "*.xml"
        self.items = list()
        self.item_names = list()  # a list of ItemNames from xml files
        self.xml_files = list()  # a list of a xml file paths
        self.exclude_list = self.get_excluded_files()

    def get_all_damn_xmls(self):
        """gets all the xmls files from a self.folder recursively"""
        for root, dirnames, filenames in os.walk(self.folder):
            for filename in fnmatch.filter(filenames, self.file_type):
                self.xml_files.append(os.path.join(root, filename))

    def get_names_from_xml(self):
        """gets all the  item names from self.xml_files"""
        for xml in self.xml_files:
            with open(os.path.normpath(xml), "r") as f:
                soup = BS(f.readline())
                self.item_names.append(soup.find("item")["name"])

    def add_xmls(self):
        """spawn in each of our items from self.item_names and then select them"""
        num_cols = 25
        x = 0
        num_added = 0
        for idx, item in enumerate(self.item_names):
            if idx % num_cols == 0:
                x += 1
            if item not in self.exclude_list:
                self.items.append(
                    general.new_object("Entity", item, "", x, idx % num_cols, 0)
                )
                num_added += 1
            else:
                idx -= 1
        print(
            "Added %s CGF Files to the map. Thanks for adding every damn entity!"
            % num_added
        )
        # clear the selection and add the new items to the selection

    def start(self):
        """main process to run after instantiating class"""
        # find all the damn cgfs
        self.get_all_damn_xmls()
        # get the names from the xml
        self.get_names_from_xml()
        # add them all to the map
        self.add_xmls()
        general.select_objects(self.items)

    @staticmethod
    def get_excluded_files():
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "excluded_entities.txt"
            ),
            "r",
        ) as f:
            return f.read().splitlines()


def main():
    eg = EntityGrabber()
    eg.start()


# run the program
if __name__ == "__main__":
    main()
