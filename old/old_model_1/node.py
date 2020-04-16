from block import Block
from chain import Chain

class Node():
	
	def __init__(self, chain, rate):
		self.chain = chain 			# pass by reference
		self.ID = chain.get_next_node_ID()
		self.rate = rate
		self.found_blocks = []
		self.visible_blocks = []

	def make_block(self):
		prev = self.chain.get_main_chain()
		self.found_blocks.append(Block(prev, self.chain.time, self.ID))

	def commit_block(self):
		if(self.found_blocks != []):
			self.chain.add_block(self.found_blocks.pop(0))
			
	def get_time(self):
		return self.chain.time