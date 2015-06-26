import os
import subprocess


def get_cvar(cvar):
	return general.get_cvar('r_displayinfo')

def set_cvar(cvar, value):
	general.set_cvar(cvar, value)

def main():
	set_cvar('r_getScreenshot', 1)

	
	try:
		path =  os.getcwd() + '\User\ScreenShots'
		command = r'explorer "%s"' % path 
		print command
		subprocess.Popen(command)
	except:
		pass





if __name__ == '__main__':
	main()