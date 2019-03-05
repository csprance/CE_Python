# Checks to make sure everything in items folder has an icon
# uses a list of excluded items/folders not to check in
# !/usr/bin/python
"""
Gets all item names from Scripts/Entities/Items
Chris Sprance
Entrada interactive
"""

# glob looks through files in a smart way
import fnmatch
import os
import re


class MisItems(object):
    """
	Grabs entities from a folder
	"""

    def __init__(self):
        super(MisItems, self).__init__()
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
        self.file_type = "*.xml"
        self.items = list()
        self.item_names = list()  # a list of ItemNames from xml files
        self.xml_files = list()  # a list of a xml file paths
        self.exclude_list = self.get_excluded_files_list()

    def get_all_xml_paths(self):
        """gets all the xmls files from a self.folder recursively"""
        for root, dirnames, filenames in os.walk(self.folder):
            for filename in fnmatch.filter(filenames, self.file_type):
                self.xml_files.append(os.path.join(root, filename))
        return self.xml_files

    def get_names_from_xml(self):
        """gets all the  item names from self.xml_files"""
        for xml in self.xml_files:
            with open(os.path.normpath(xml), "r") as f:
                x = re.findall(r'"(.*?)"', f.readline())
                if len(x) > 0:
                    self.item_names.append(x[0])
        return self.item_names

    def get_all_names(self):
        """main process to run after instantiating class"""
        # find all the damn cgfs
        self.get_all_xml_paths()
        # get the names from the xml
        self.get_names_from_xml()
        return self.item_names

    @staticmethod
    def get_excluded_files_list():
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "excluded_entities.txt"
            ),
            "r",
        ) as f:
            return f.read().splitlines()


class MisIcons(object):
    """
	Grabs entities from a folder
	"""

    def __init__(self):
        super(MisIcons, self).__init__()
        self.folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "GameSDK",
                "Libs",
                "UI",
                "Inventory",
                "item_images",
            )
        )
        self.file_type = "*_48.png"
        self.names = list()  # a list of Icon Names from png files
        self.files = list()  # a list of a png file paths

    def get_all_icon_paths(self):
        """gets all the xmls files from a self.folder recursively"""
        for root, dirnames, filenames in os.walk(self.folder):
            for filename in fnmatch.filter(filenames, self.file_type):
                self.files.append(os.path.join(root, filename))
        return self.files

    def get_icon_names(self):
        """strips off directory info and _48.png"""
        for icon_path in self.files:
            self.names.append(os.path.basename(icon_path).replace("_48.png", ""))
        return self.names

    def get_all_names(self):
        """main process to run after instantiating class"""
        # find all the icon files
        self.get_all_icon_paths()
        # get the names from the icon files
        self.get_icon_names()
        return self.names


def get_icons():
    return ""


def main():
    # a list of item class names
    items = MisItems().get_all_names()
    # a list of icons currently
    icons = MisIcons().get_all_names()
    # any icon that is not in items and is not in excluded items
    missing_icons = [icon for icon in icons if icon not in items]
    for missing_icon in missing_icons:
        print(missing_icon)


if __name__ == "__main__":
    main()
