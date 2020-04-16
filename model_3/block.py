class Block():

	def __init__(self, prev, timestamp, owner, height):
		self.prev = prev
		self.timestamp = timestamp
		self.owner = owner
		self.height = height
		self.ID = 0			    # Assigned by the chain upon committing
		# self.data = data 		# Assume there's no data for simplicity
		# self.nonce = 0		# The proof of work is omitted for simplicity
		# self.hash = ""