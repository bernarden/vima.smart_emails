from datetime import datetime
from typing import List

from smart_emails.domain.attribute import Attribute


class Run:
	def __init__(self, attributes: List[Attribute], date: datetime):
		self.attributes = attributes
		self.date = date

	def __repr__(self):
		return "Test run: %s" % self.attributes
