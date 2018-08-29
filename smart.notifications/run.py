class Run:
	def __init__(self, attributes, date):
		self.attributes = attributes
		self.date = date

	def __repr__(self):
		return "Test run: %s" % (self.attributes)
