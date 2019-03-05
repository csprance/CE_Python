import os

import general

if __name__ == "__main__":
    x, y, z = [round(x, 4) for x in general.get_selection_center()]
    command = "echo %s,%s,%s | clip" % (x, y, z)
    os.system(command)
