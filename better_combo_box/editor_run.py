import subprocess
import os


def get_combo_selection(options=[""]):
    return subprocess.check_output(
        os.path.abspath("Editor/Scripts/better_combo_box/dist/better_combo_box.exe")
        + " %s" % ("|".join(options))
    )
