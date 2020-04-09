import random
from chain import Chain
from node import Node
from block import Block

NUM_NODES = 10
MAX_TIME = 2

def main():

	# create a blockchain
	chain = Chain()

	# initialize set of nodes
	nodes = []
	for i in range(NUM_NODES):
		nodes.append(Node(chain, 1))
	
	# actions
	while chain.time <= MAX_TIME:
		for i in range(NUM_NODES):
			cur_node = random.choice(nodes)
			cur_node.make_block()
			cur_node.commit_block()
			chain.inc_time()

	chain.print_main_chain_head()

	nodes[0].found_blocks.append(Block(chain.blocks[6], chain.time, nodes[0].ID))
	nodes[0].commit_block()
	chain.print_main_chain_head()

	for i in range(11, 25):
		nodes[0].found_blocks.append(Block(chain.blocks[i], chain.time, nodes[0].ID))
		nodes[0].commit_block()
		chain.print_main_chain_head()

	chain.print_chain()

	for i in range(chain.main_chain_max_height):
		chain.print_chain_converge_at_height(i)

if __name__ == '__main__':
	main()