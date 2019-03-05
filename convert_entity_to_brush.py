#!/usr/bin/python
"""
Convert an entity into a brush
Chris Sprance
Entrada interactive
"""

# glob looks through files in a smart way
import general


class ConvertEntityToBrush(object):
	"""
	takes the selected entities and converts them into brushes
	"""

	def __init__(self):
		super(ConvertEntityToBrush, self).__init__()
		self.selected = list()
		self.entity = str()

	def start(self):
		"""method called when button is pushed
		kicks the whole thing off"""
		# get and store the selection
		self.selected = general.get_names_of_selected_objects()
		# loop through the selection
		for self.entity in self.selected:
			# get the items geometry file
			general.get_entity_property(self.entity, '')


if __name__ == '__main__':
	ceb = ConvertEntityToBrush()
	ceb.start()
