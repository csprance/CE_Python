import general

# get the list of all of our objects
class SimBrush(object):
	"""
	This class holds all the relevant info for the brush and it's temporary physics 
	object created with it
	"""
	def __init__(self, pos,rot,scale, model, physobj):
		super(SimBrush, self).__init__()
		self.pos = pos
		self.rot = rot
		self.scale = scale
		self.model = model
		self.physobj = physobj


objname = general.get_names_of_selected_objects()
for x in objname:
	print x