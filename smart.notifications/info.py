class Info:
	def __init__(self, values):
		self.model_family = values[0]
		self.device_model = values[1]
		self.serial_number = values[2]
		self.lu_wwn_device_id = values[3]
		self.firmware_version = values[4]
		self.user_capacity = values[5]
		self.sector_size = values[6]
		self.device_is = values[7]
		self.ata_version_is = values[8]
		self.local_time_is = values[9]
		self.smart_support_available = values[10]
		self.smart_support_enabled = values[11]


	def __repr__(self):
		return "INFO: \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s" % (self.model_family,
		self.device_model,
		self.serial_number,
		self.lu_wwn_device_id,
		self.firmware_version,
		self.user_capacity,
		self.sector_size,
		self.device_is,
		self.ata_version_is,
		self.local_time_is,
		self.smart_support_available,
		self.smart_support_enabled)

