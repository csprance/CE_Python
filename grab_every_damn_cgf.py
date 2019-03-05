#!/usr/bin/python
"""
Go through and place all entities from a folder into a scene
Chris Sprance
Entrada interactive
"""
import general
import fnmatch
import os
import re


class EntityGrabber(object):
    """Grabs entities from a folder and places them in the sandbox editor This is because a lot of time you need to
	test a lot of items and dragging them by hand blows! On Script Activation it will Open a file dialog and ask you to
	choose a folder full of entities you would like to spawn These xml files will be scanned for there item names and
	that will be used to spawn items in a short distance from each other and then select them all so you can quickly
	shift click to place the lot of items"""

    def __init__(self):
        super(EntityGrabber, self).__init__()
        general.clear_selection()
        self.folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "GameSDK", "Objects")
        )
        self.file_type = "*.cgf"
        self.cgf_files = list()  # a list of cgf paths
        self.items = list()
        self.increment_amount = 0

    def get_all_damn_cgfs(self):
        """gets all the cgfs files from a self.folder recursively"""
        for root, dirnames, filenames in os.walk(self.folder):
            for filename in fnmatch.filter(filenames, self.file_type):
                self.items.append(os.path.join(root, filename))

    @staticmethod
    def norm_path_for_ce(path):
        split_path = os.path.normpath(path).split(os.path.sep)
        for idx, part in enumerate(split_path):
            if part == "GameSDK":
                return "/".join(split_path[idx + 1 :])

    def add_cgfs(self):
        """spawn in each of our items from self.item_names and then select them"""
        num_cols = 25
        x = 0
        for idx, item in enumerate(self.items):
            if idx % num_cols == 0:
                # increment by some amount set by the last objects x width
                x += self.increment_amount
            general.select_object(
                general.new_object(
                    "Brush",
                    self.norm_path_for_ce(item),
                    "",
                    x,
                    (idx % num_cols) * 55,
                    32,
                )
            )
            self.set_increment_amount()
        print(
            "Added %s CGF Files to the map. Thanks for adding every damn CGF!"
            % len(self.items)
        )

        # clear the selection and add the new items to the selection

    def start(self):
        """main process to run after instantiating class"""
        # find all the damn cgfs
        self.get_all_damn_cgfs()
        # filter out all the ones we don't want
        self.filter_cgfs()
        # print self.items
        # add them all to the map
        self.add_cgfs()

    def set_increment_amount(self):
        x1, y1, z1, x2, y2, z2 = general.get_selection_aabb()
        # width of x + 1/2 width of x because it measures from center point
        self.increment_amount = (x2 - x1) + ((x2 - x1) * 0.5)
        general.clear_selection()

    def filter_cgfs(self):
        """filter out the cgfs from self.items"""
        regex = re.compile(r".*_lod[0-9]")
        dws_items_re = re.compile(r"dws_.*")
        # # get non lod
        self.items = [item for item in self.items if regex.search(item) is not True]
        # # get only lods
        # self.items = filter(regex.search, self.items)
        # # get only dws
        # self.items = [item for item in self.items if dws_items_re.search(item) is not True]


def main():
    eg = EntityGrabber()
    eg.start()


# run the program
if __name__ == "__main__":
    main()
