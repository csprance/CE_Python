from better_cry import Level
import subprocess


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    level = Level()
    print('\n'.join([item.geometry_file for item in level.selected]))
