import random
from block import Block

class Chain():

	def __init__(self):
		self.delayFactor = 3 				# used for calculating the score
		self.time = 1						# current time (discrete, integers)
		self.block_ID = 0 					# keep track of the number of blocks
		self.node_ID = 0 					# keep track of the number of nodes
		self.blocks = []					# all the blocks in the chain
		# self.max_height = 1				# max block height (not necessarily an chain with score 0)
		# self.main_chain_max_height = 1	# max block height with score zero
		self.add_genesis_block()

	def inc_time(self):
		self.time += 1

	def get_next_block_ID(self):
		self.block_ID += 1
		return self.block_ID

	def get_next_node_ID(self):
		self.node_ID += 1
		return self.node_ID

	def get_block(self, ID):
		return self.blocks[ID]

	def add_genesis_block(self):
		genesis_block = Block(-1, 0, 0, 1) # prev = -1
		genesis_block.ID = 0
		# genesis_block.score = 0
		self.blocks.append(genesis_block)

	def add_block(self, block): 				# add block to the chain
		block.ID = self.get_next_block_ID() 	# non-genesis block starts from 1
		prev_block = self.get_block(block.prev)
		block.height = prev_block.height + 1
		self.blocks.append(block)

	def print_block(self, b):
		print("ID: ", b.ID, "\t prev: ", b.prev, "\t height: ", b.height, "\t timestamp: ", b.timestamp, "\t owner: ", b.owner)

	def print_chain(self):
		for b in self.blocks:
			self.print_block(b)
	
			