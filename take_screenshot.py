import os
import subprocess

import general


def set_cvar(cvar, value):
    general.set_cvar(cvar, value)


def take_screenshot(open_folder=True):
    general.set_cvar('r_getScreenshot', 1)
    if open_folder:
        try:
            path = os.getcwd() + '\User\ScreenShots'
            command = r'explorer "%s"' % path
            print(command)
            subprocess.Popen(command)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    take_screenshot()
