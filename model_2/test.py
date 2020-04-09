from network import Network
import random

net = Network(10)

net.gen_random_graph(0, 10)

rand_nodes_order = list(range(10))
print(rand_nodes_order)
random.shuffle(rand_nodes_order)
print(rand_nodes_order)