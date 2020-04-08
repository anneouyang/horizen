from chain import Chain
from node import Node
from block import Block

NUM_NODES = 10
MAX_TIME = 2

def main():

	# create blockchain
	chain = Chain()

	# initialize set of nodes
	nodes = []
	for i in range(NUM_NODES):
		nodes.append(Node(chain, 1))
	
	# actions
	while chain.time <= MAX_TIME:
		for i in range(NUM_NODES):
			nodes[i].make_block()
			nodes[i].commit_block()
		chain.inc_time()

	nodes[0].found_blocks.append(Block(chain.blocks[9], chain.time, nodes[0].ID))
	nodes[0].commit_block()

	chain.print_chain()


if __name__ == '__main__':
	main()