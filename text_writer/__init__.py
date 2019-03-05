"""
This script will call for user input and then
create a text cgf object for that string
Then it will save that object to a file name
in a folder with the string input as the
cgf name.

* run the script
* get user input
* split up the user input into the individual chars
* create the text planes (import binary data from grp and use that instead of requiring the objects exist already.)
* merge the text planes together,
* export the object as the user_string.cgf
* bring the object into the scene and select it
* place it at the cursor
"""
import general

# Text Constants
TEXT_HEIGHT = 3.7
TEXT_WIDTH = 2.160
# all available characters to select
CHARACTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "!",
    "$",
    ",",
    "-",
    ".",
    "/",
    "@",
    "?",
    ">",
]


# Writes text into a designer object
class TextWriter(object):

    def __init__(self):
        super(TextWriter, self).__init__()
        self.check_if_text_layer_present()
        self.text = self.get_input()

    def start(self):
        if not general.is_layer_exist("font_bebas_neau"):
            general.message_box_ok(
                "Please Import Editor/Python/Scripts/text_writer/font_bebas_neau.lyr"
            )
        else:
            return self.create_designer_text()

    @staticmethod
    def get_input():
        return list(general.edit_box("Text to Write").upper())

    @staticmethod
    def check_if_text_layer_present():
        if not general.is_layer_exist("font_bebas_neau"):
            general.message_box_ok(
                "Please Import Editor/Python/Scripts/text_writer/font_bebas_neau.lyr"
            )
            return False

    @staticmethod
    def select_copy_paste(letter="", index=0):
        """
        select and copy our polygon item then return to original item and selCopyPast
        :param letter: letter to select
        :param index: position of the current letter
        :return: None
        """
        general.clear_selection()
        general.select_object(letter)
        general.set_position(letter, 0, -TEXT_WIDTH * index, 0)

    @staticmethod
    def build_text_list_with_counts(text):
        return_list = []
        string_builder = ""
        for letter in text:
            if letter is " ":
                return_list.append(" ")
            if letter in CHARACTERS:
                string_builder += letter
                return_list.append("%s_%s" % (letter, string_builder.count(letter)))
        return return_list

    def create_designer_text(self):
        # loop through our text and do the things to the letters
        letters = self.build_text_list_with_counts(self.text)
        for idx, letter in enumerate(letters):
            if letter is not " ":
                self.select_copy_paste(letter, idx)
        # select the letters we used
        general.clear_selection()
        general.select_objects(filter(lambda char: char is not " ", letters))


if __name__ == "__main__":
    tw = TextWriter()
    tw.start()
