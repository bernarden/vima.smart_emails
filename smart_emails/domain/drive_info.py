class DriveInfo:
	def __init__(self, values: {}):
		self.values = values

	@property
	def model_family(self) -> str:
		return self.values.get('Model Family:', "N/A")

	@property
	def device_model(self) -> str:
		return self.values.get('Device Model:', "N/A")

	@property
	def serial_number(self) -> str:
		return self.values.get('Serial Number:', "N/A")

	@property
	def lu_wwn_device_id(self) -> str:
		return self.values.get('LU WWN Device Id:', "N/A")
	
	@property
	def firmware_version(self) -> str:
		return self.values.get('Firmware Version:', "N/A")

	@property
	def user_capacity(self) -> str:
		return self.values.get('User Capacity:', "N/A")

	@property
	def sector_size(self) -> str:
		return self.values.get('Sector Size:', "N/A")

	@property
	def sector_sizes(self) -> str:
		return self.values.get('Sector Sizes:', "N/A")

	@property
	def rotation_rate(self) -> str:
		return self.values.get('Rotation Rate:', "N/A")

	@property
	def device_is(self) -> str:
		return self.values.get('Device is:', "N/A")

	@property
	def ata_version_is(self) -> str:
		return self.values.get('ATA Version is:', "N/A")

	@property
	def sata_version_is(self) -> str:
		return self.values.get('SATA Version is:', "N/A")

	@property
	def local_time_is(self) -> str:
		return self.values.get('Local Time is:', "N/A")

	@property
	def smart_support_enabled(self) -> str:
		return self.values.get('Smart support is:', "N/A")

	def __repr__(self):
		return "INFO: \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s" % (self.model_family,
		self.device_model,
		self.serial_number,
		self.lu_wwn_device_id,
		self.firmware_version,
		self.user_capacity,
		self.sector_size,
		self.rotation_rate,
		self.device_is,
		self.ata_version_is,
		self.local_time_is,
		self.smart_support_enabled)

