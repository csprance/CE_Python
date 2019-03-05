import subprocess
import os
import general


def main():
    cwd = os.getcwd()
    if "Steam" in cwd:
        general.message_box_ok("Remove your Hard link it is no longer needed")
        return "nothing"
    os.chdir("EI/Tools/Atlas/map")
    subprocess.call(["nw.exe"])
    os.chdir(cwd)


if __name__ == "__main__":
    main()
