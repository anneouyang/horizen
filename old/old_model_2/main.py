import random
import matplotlib.pyplot as plt
from chain import Chain
from node import Node
from block import Block
from network import Network

NUM_NODES = 10
MAX_TIME = 1000

def main():

	# create a blockchain
	chain = Chain()

	# create a network of nodes
	network = Network(NUM_NODES)
	network.gen_random_graph(0, 100)

	# initialize set of nodes
	nodes = []
	for i in range(NUM_NODES):
		nodes.append(Node(chain, 1, network))
	
	# actions
	rand_nodes_order = list(range(NUM_NODES))
	prev_height = 1
	x = []
	y = []
	while chain.time <= MAX_TIME:
		# print(rand_nodes_order)
		random.shuffle(rand_nodes_order)
		num_nodes_at_this_time = random.randint(1, NUM_NODES)
		# print(num_nodes_at_this_time, len(rand_nodes_order), len(nodes))
		for i in range(num_nodes_at_this_time):
			cur_node = nodes[rand_nodes_order[i]]
			cur_node.make_block()
			cur_node.commit_blocks()
		chain.inc_time()
		if(chain.chain_converge() and chain.main_chain_max_height != prev_height):
			y.append(chain.main_chain_max_height)
			x.append(chain.time)
			print("Chain converges at height", chain.main_chain_max_height, "\t time:", chain.time)
			prev_height = chain.main_chain_max_height

	plt.plot(x, y)
	plt.xlabel("time")
	plt.ylabel("main chain height")
	plt.show()
	chain.print_chain()

	# for i in range(chain.main_chain_max_height):
	# 	chain.print_chain_converge_at_height(i)

if __name__ == '__main__':
	main()