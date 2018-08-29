class Attribute:
	def __init__(self, values):
		self.id = values[0]
		self.name = values[1]
		self.flag = values[2]
		self.value = values[3]
		self.worst = values[4]
		self.thresh = values[5]
		self.att_type = values[6]
		self.updated = values[7]
		self.when_failed = values[8]
		self.raw_value = values[9]

	def __repr__(self):
		return "ATTRIBUTES: \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s" % (self.id,
		self.name,
		self.flag ,
		self.value,
		self.worst,
		self.thresh,
		self.att_type,
		self.updated,
		self.when_failed,
		self.raw_value)
