import json
import sys
import tkinter
from tkinter.filedialog import askopenfilename, askdirectory


if __name__ == "__main__":
    root = tkinter.Tk()
    root.withdraw()
    file_types = sys.argv[1]
    initial_dir = sys.argv[2]
    if len(sys.argv) > 3:
        select_folder = sys.argv[3]
    else:
        select_folder = False
    if select_folder:
        file_path = askdirectory(
            title="Select Folder(s)",
            initialdir=sys.argv[2],
        )
        print(json.dumps(file_path))
    else:
        file_path = askopenfilename(
            title="Select File(s)",
            multiple=True,
            filetypes=[(sys.argv[1], sys.argv[1])],
            initialdir=sys.argv[2],
        )
        print(json.dumps(file_path))
