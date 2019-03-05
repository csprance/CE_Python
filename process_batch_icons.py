# takes the screenshot for an icon
import os
import subprocess

from cry_utils.get_files_by_type import get_all_files


def space_seperator(arr):
	x = ''
	for item in arr:
		x += ' ' + item + ' '
	return x


def remove_top_line(f):
	with open(f, 'r') as fin:
		data = fin.read().splitlines(True)
	with open(f, 'w') as fout:
		fout.writelines(data[1:])


def capture():
	scripts_dir = os.path.abspath(os.path.dirname(__file__))
	screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'user', 'screenshots'))
	images = get_all_files('.jpg', screenshot_dir)
	with open(scripts_dir + '//iconfile_done.txt') as infile:
		data = infile.read().splitlines(True)
		for x in data:
			subprocess.Popen('python %s %s --args %s' % (
				scripts_dir + '\\icon_object_create_icon.py', x.split(',')[1], space_seperator(images)))


if __name__ == '__main__':
	capture()
