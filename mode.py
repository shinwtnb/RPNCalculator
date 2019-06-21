import enum

class Mode():
	class Modes(enum.Enum):
		editting = enum.auto()
		fixed= enum.auto()
	__current__ = Modes.editting
			
		
	def isEditting():
		return  Mode.__current__ == Mode.Modes.editting
	
	def isFixed():
		return  Mode.__current__ == Mode.Modes.fixed
			
	def setEditting():
		Mode.__current__ = Mode.Modes.editting
	
	def setFixed():
		Mode.__current__ = Mode.Modes.fixed

