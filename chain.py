import random
from block import Block

class Chain():

	def __init__(self):
		self.delayFactor = 1
		self.time = 1
		self.block_ID = 0
		self.node_ID = 0
		self.blocks = []
		self.max_height = 1
		self.main_chain_max_height = 1
		self.add_genesis_block()

	def inc_time(self):
		self.time += 1

	def get_next_block_ID(self):
		self.block_ID += 1
		return self.block_ID

	def get_next_node_ID(self):
		self.node_ID += 1
		return self.node_ID

	def get_main_chain(self):
		max_height_blocks = [b for b in self.blocks if (b.height == self.main_chain_max_height and b.score <= 0)]
		return random.choice(max_height_blocks)

	def chain_converge(self):
		max_height_blocks = [b for b in self.blocks if (b.height == self.main_chain_max_height and b.score <= 0)]
		return len(max_height_blocks) == 1

	def delay_function(self, block):
		height_diff = self.main_chain_max_height - block.height
		penalty = (-1 if height_diff < 0 else height_diff * self.delayFactor)
		main_chain_head = self.get_main_chain()
		if(main_chain_head.ID == block.prev or main_chain_head.ID == block.prev.ID):
			penalty = 0
		return penalty

	def add_genesis_block(self):
		genesis_block = Block(-1, 0, 0)
		genesis_block.ID = 0
		genesis_block.height = 1
		genesis_block.score = 0
		self.blocks.append(genesis_block)

	def add_block(self, block):
		block.ID = self.get_next_block_ID()
		# for b in self.blocks:
		# 	print(b.ID, block.prev.ID)
		prev_block = [b for b in self.blocks if b.ID == block.prev.ID]
		# print(prev_block)
		if(prev_block == []):
			return
		prev_block = prev_block[0]
		block.height = prev_block.height + 1
		self.max_height = max(self.max_height, block.height)
		block.score = prev_block.score + self.delay_function(block)
		if(block.score <= 0):
			self.main_chain_max_height = max(self.main_chain_max_height, block.height)
		self.blocks.append(block)

	def print_gen_block(self, b):
		print("ID: ", b.ID, "\t prev: ", b.prev, "\t score: ", b.score, "\t height: ", b.height, "\t timestamp: ", b.timestamp, "\t owner: ", b.owner)

	def print_block(self, b):
		print("ID: ", b.ID, "\t prev: ", b.prev.ID, "\t score: ", b.score, "\t height: ", b.height, "\t timestamp: ", b.timestamp, "\t owner: ", b.owner)

	def print_chain(self):
		for b in self.blocks:
			if b.ID == 0:
				self.print_gen_block(b)
			else:
				self.print_block(b)
			print(self.chain_converge())
			