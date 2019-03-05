# clears all the log files
import general

import glob
import os

root = os.getcwd()
logs = list()
msg = "Delete Logs: "

for f in glob.glob("*.log"):
    logs.append(os.path.join(root, f))
    msg += "\n " + os.path.join(root, f)

if general.message_box_yes_no(msg):
    for log in logs:
        try:
            os.remove(log)
        except:
            pass
