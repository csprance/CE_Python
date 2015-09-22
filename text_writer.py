# This script will call for user input and then 
# create a text cgf object for that string
# Then it will save that object to a file name 
# in a folder with the string input as the
# cgf name.
# Chris Sprance
# Entrada Interactive
from crypy import *

values = general.edit_box('Text to Write')
# run the script

# get user input 

# split up the user input into the individual chars

# create the text planes (import binary data from grp and use that instead of requiring the objects exist already.)

# merge the text planes together,

# export the object as the user_string.cgf

# bring the object into the scene and select it 
# and place it at the cursor



class TextWriter(object):
	"""This is the class used to create the 
	text objects"""
	def __init__(self):
		super(TextWriter, self).__init__()
		
	def get_input(self):
		pass



def main():
	pass


if __name__ == '__main__':
	main()