import unittest

from icon_object_db import IconObjectDB


class MyTestCase(unittest.TestCase):
	def test_something(self):
		io = IconObjectDB()
		x = io.get_all()
		objs = list()
		for obj in io.get_all():
			if 'brush' in obj:
				objs.append(obj['brush'])
		print objs



if __name__ == '__main__':
	unittest.main()
