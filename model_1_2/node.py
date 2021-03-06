import random
from block import Block
from chain import Chain
from network import Network

class Node():
	
	def __init__(self, chain, rate, network, delay = 0):
		self.NOTVISIBLE = 99999999
		self.chain = chain 			# pass by reference
		self.ID = chain.get_next_node_ID()
		self.rate = rate
		self.net = network
		self.delay = delay 			# unnecessary for now
		self.found_blocks = []
		self.scores = [0] 			# node's view of the blockchain, objective scoring of blocks; 99999999 means block is not visible to the node yet
		self.cur_max_height = 1
		self.delayFactor = 1

	
	def get_score(self, block):
		# print(block.ID, block.prev)
		return self.scores[self.chain.blocks[block.ID].prev] + self.delay_function(block)

	def delay_function(self, block):
		height_diff = self.cur_max_height - block.height
		penalty = (-1 if height_diff < 0 else height_diff * self.delayFactor)
		chain_heads = self.get_chain_heads()
		# print("chain heads", chain_heads)
		chain_heads = [h.ID for h in chain_heads]
		if(block.prev in chain_heads):
			# print("zero pen")
			penalty = 0
		return penalty

	def update_visible_blocks(self):
		if (len(self.chain.blocks) > len(self.scores)):
			self.scores.extend([self.NOTVISIBLE for i in range(len(self.chain.blocks) - len(self.scores))])		# ensure that every score element correponds to a block
		for block in self.chain.blocks:
			if(block.prev != -1 and self.scores[block.prev] == self.NOTVISIBLE):
				continue
				# raise ValueError('Error: a dangling block', block.ID, block.prev)
			ind = block.ID
			if self.scores[ind] == self.NOTVISIBLE and block.timestamp <= self.chain.time - self.net.A[self.ID - 1][block.owner - 1]: # newly found block and taking into account the network delay
				self.scores[ind] = self.get_score(block)
				# print(self.scores[ind])
				if(self.scores[ind] <= 0):
					self.cur_max_height = max(self.cur_max_height, block.height)

	def get_chain_heads(self):
		ret = []
		for block in self.chain.blocks:
			if(block.ID >= len(self.scores)):
				break
			# print(self.scores[block.ID], block.height, self.cur_max_height)
			if(self.scores[block.ID] == self.NOTVISIBLE):
				continue
			if(block.height == self.cur_max_height and self.scores[block.ID] <= 0): # only blocks with score <= 0 are valid
				ret.append(block)
		# print("ret size", len(ret))
		return ret

	def get_chain_head(self):
		return random.choice(self.get_chain_heads())

	def make_block(self):
		prev = self.get_chain_head()
		self.found_blocks.append(Block(prev.ID, self.chain.time, self.ID, prev.height + 1))

	# account for different computing power (defined by rate)
	def make_blocks(self):
		for i in range(self.rate):
			self.update_visible_blocks()
			self.make_block()
			self.commit_blocks()

	def commit_blocks(self):
		if(self.found_blocks != []):
			blocks_to_commit = [b for b in self.found_blocks if (b.timestamp + self.delay) <= self.chain.time]
			while(blocks_to_commit != []):
				self.chain.add_block(blocks_to_commit.pop(0))
		self.found_blocks = [b for b in self.found_blocks if (b.timestamp + self.delay) > self.chain.time]


	def print_block(self, b):
		print("ID: ", b.ID, "\t prev: ", b.prev, self.chain.blocks[b.prev].owner, "\t score: ", self.scores[b.ID], "\t height: ", b.height, "\t timestamp: ", b.timestamp, "\t owner: ", b.owner)

	def print_chain(self):
		for b in self.chain.blocks:
			if b.ID >= len(self.scores):
				break
			if self.scores[b.ID] == self.NOTVISIBLE:
				continue
			self.print_block(b)
			