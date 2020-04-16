import random
import matplotlib.pyplot as plt
from collections import Counter
from chain import Chain
from node import Node
from block import Block
from network import Network

NUM_NODES = 10
MAX_TIME = 100
CATCH_UP_TIME = 50
MIN_DELAY, MAX_DELAY = 0, 50

def converge_number(l):
	return Counter(l).most_common(1)[0][1]

def main():

	# create a blockchain
	chain = Chain()

	# create a network of nodes
	network = Network(NUM_NODES)
	# network.gen_random_graph(MIN_DELAY, MAX_DELAY)
	graph = [	[0, 0, 0, 0, 0, 999, 999, 999, 999, 999],
				[0, 0, 0, 0, 0, 999, 999, 999, 999, 999],
				[0, 0, 0, 0, 0, 999, 999, 999, 999, 999],
				[0, 0, 0, 0, 0, 999, 999, 999, 999, 999],
				[0, 0, 0, 0, 0, 30, 999, 999, 999, 999],
				[999, 999, 999, 999, 30, 0, 0, 0, 0, 0],
				[999, 999, 999, 999, 999, 0, 0, 0, 0, 0],
				[999, 999, 999, 999, 999, 0, 0, 0, 0, 0],
				[999, 999, 999, 999, 999, 0, 0, 0, 0, 0],
				[999, 999, 999, 999, 999, 0, 0, 0, 0, 0]	]
	network.set_graph(graph)

	# initialize set of nodes
	nodes = []
	for i in range(NUM_NODES):
		nodes.append(Node(chain, 1, network))
	
	# actions
	rand_nodes_order = list(range(NUM_NODES))
	prev_height = 1
	x = []
	y = []
	z = []
	nodes[0].rate = 10
	while chain.time <= MAX_TIME:
		print(chain.time)
		random.shuffle(rand_nodes_order)
		num_nodes_at_this_time = random.randint(NUM_NODES, NUM_NODES)

		for i in range(num_nodes_at_this_time):
			cur_node = nodes[rand_nodes_order[i]]
			# cur_node.update_visible_blocks()
			cur_node.make_blocks()
			# cur_node.commit_blocks()

		for i in range(NUM_NODES):
			nodes[i].update_visible_blocks()

		chain.inc_time()

		heads = []
		for node in nodes:
			hd = node.get_chain_heads()
			heads.extend([nn.ID for nn in hd])
		# print(Counter(heads).most_common(NUM_NODES))
		conv_num = converge_number(heads)
		y.append(conv_num * 1.0 / NUM_NODES)
		x.append(chain.time)
		z.append(len([l for l in Counter(heads).most_common(NUM_NODES) if l[1] == conv_num]) / 1)

	while chain.time <= MAX_TIME + CATCH_UP_TIME:
		print(chain.time)
		for i in range(NUM_NODES):
			nodes[i].update_visible_blocks()
		chain.inc_time()

		heads = []
		for node in nodes:
			hd = node.get_chain_heads()
			heads.extend([nn.ID for nn in hd])
		# print(Counter(heads).most_common(NUM_NODES))
		conv_num = converge_number(heads)
		y.append(conv_num * 1.0 / NUM_NODES)
		x.append(chain.time)
		z.append(len([l for l in Counter(heads).most_common(NUM_NODES) if l[1] == conv_num]) / 1)

	# chain.print_chain()

	# for node in nodes:
	# 	node.print_chain()


	plt.subplot(2, 1, 1)
	plt.plot(x, y)
	plt.xlabel("time")
	plt.ylabel("max % nodes agreeing on some head")
	plt.subplot(2, 1, 2)
	plt.plot(x, z)
	plt.xlabel("time")
	plt.ylabel("number of heads")
	plt.show()
	# chain.print_chain()

	# for i in range(chain.main_chain_max_height):
	# 	chain.print_chain_converge_at_height(i)

if __name__ == '__main__':
	main()