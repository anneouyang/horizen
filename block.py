class Block():

	def __init__(self, prev, timestamp, owner):
		self.prev = prev
		self.timestamp = timestamp
		self.owner = owner
		# self.data = data 		# Assume there's no data for simplicity
		self.ID = 0			    # Attributes assigned by the chain upon committing
		self.height = 0
		self.score = 0
		# self.nonce = 0		# Assume the proof of work is always valid for simplicity
		# self.hash = ""