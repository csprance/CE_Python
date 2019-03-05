import subprocess
import os


def get_file_path_list(file_type, initial_dir, folder=''):
    return map(
        lambda x: os.path.normpath(x).replace('"', '').strip(),
        subprocess.check_output(
            os.path.abspath(
                "Editor/Scripts/better_file_dialog/dist/better_file_dialog.exe"
            )
            + " %s %s %s" % (file_type, initial_dir, folder)
        )
        .strip()[1:-1]
        .split(","),
    )
