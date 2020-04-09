import random
from block import Block
from chain import Chain
from network import Network

class Node():
	
	def __init__(self, chain, rate, network):
		self.chain = chain 			# pass by reference
		self.ID = chain.get_next_node_ID()
		self.rate = rate
		self.net = network
		self.found_blocks = []
		self.visible_blocks = []

	def update_visibile_blocks():
		self.visible_blocks = [self.chain.blocks[0]]
		my_id = self.ID - 1
		n = self.net.num_nodes
		for i in range(n):
			if i == my_id:
				continue
			self.visible_blocks.extend([b for b in chain.blocks if ((b.owner == i + 1) and (b.timestamp <= self.chain.time - net.A[my_id][i]))])

	def get_chain_head():
		cur_height = 1
		heads = [self.chain.blocks[0]]
		for b in self.visible_blocks:
			if b.score < 0:
				continue
			if(b.height > cur_height):
				heads = []
				heads.append(b)
				cur_height = b.height
			elif(b.height == cur_height):
				heads.append(b)
		return random.choice(heads)

	def make_block(self):
		self.update_visibile_blocks()
		# prev = self.chain.get_main_chain()
		prev = self.get_chain_head()
		self.found_blocks.append(Block(prev, self.chain.time, self.ID))

	def commit_blocks(self):
		if(self.found_blocks != []):
			blocks_to_commit = [b for b in self.found_blocks if (b.timestamp + self.delay) <= self.chain.time]
			if(blocks_to_commit != [])
			for b in blocks_to_commit:
				self.chain.add_block(b.pop(0))
		self.found_blocks = [b for b in self.found_blocks if (b.timestamp + self.delay) > self.chain.time]
			
	def get_time(self):
		return self.chain.time