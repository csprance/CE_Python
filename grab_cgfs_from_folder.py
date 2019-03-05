#!/usr/bin/python
"""
Get any number of cgf files to add to the map
Chris Sprance
Entrada interactive
"""

import os
import general
from better_file_dialog.editor_run import get_file_path_list


class CGFGrabber(object):
    """
    Grabs cgfs from a folder and places them in the sandbox editor
    This is because a lot of time you need to test a lot of items and dragging them by hand blows!
    On Script Activation it will Open a file dialog and ask you to choose a folder full of cgfs
    """

    def __init__(self):
        super(CGFGrabber, self).__init__()
        general.clear_selection()
        self.folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "GameSDK", "Objects")
        )
        self.file_type = ".cgf"
        self.cgf_files = list()  # a list of normalized cgf paths
        self.items = (
            list()
        )  # list of all names added in from created objects so you can select
        self.increment_amount = 0

    def get_user_input(self):
        """calls the function that opens our file dialog and returns a directory"""
        self.cgf_files = get_file_path_list(
            self.file_type, os.path.abspath(r"GameSDK\Objects")
        )

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
        for idx, item in enumerate(self.cgf_files):
            if idx % num_cols == 0:
                # increment by some amount set by the last objects x width
                x += self.increment_amount
            ob = general.new_object(
                "Brush", self.norm_path_for_ce(item), "", x, (idx % num_cols) * 0.23, 32
            )
            self.items.append(ob)
            general.select_object(ob)
            self.set_increment_amount()
        general.log("Added %s CGF Files to the map." % len(self.cgf_files))
        # clear the selection and add the new items to the selection

    def set_increment_amount(self):
        x1, y1, z1, x2, y2, z2 = general.get_selection_aabb()
        # width of x + 1/2 width of x because it measures from center point
        self.increment_amount = (x2 - x1) + ((x2 - x1) * 0.5)
        general.clear_selection()

    def start(self):
        """main process to run after instantiating class"""
        # get the list of cgf files
        self.get_user_input()
        # add them all to the map
        self.add_cgfs()
        general.select_objects(self.items)


# run the program
if __name__ == "__main__":
    eg = CGFGrabber()
    eg.start()
