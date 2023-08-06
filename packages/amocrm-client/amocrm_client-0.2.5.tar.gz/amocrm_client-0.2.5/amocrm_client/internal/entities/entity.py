from ..amo.amo import AMO


class Entity:
	_instance = None

	def __init__(self, config=None):
		self.config = config

	def __new__(cls, config=None):
		if not cls._instance:
			cls._instance = object.__new__(cls)
		return cls._instance

	def amo_init(self, config=None):
		if config:
			self.config = config
		return AMO(
			self.config[0],
			self.config[1],
		)
