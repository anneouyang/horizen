import random

class Network():

	def __init__(self, num_nodes):
		self.num_nodes = num_nodes
		self.A = [[0 for j in range(num_nodes)] for i in range(num_nodes)]

	def gen_random_graph(self, min_delay, max_delay):
		for i in range(self.num_nodes):
			for j in range(i + 1, self.num_nodes):
				if i == j:
					continue
				self.A[i][j] = random.randint(min_delay, max_delay + 1)
				self.A[j][i] = self.A[i][j]
		# self.print_graph()
		self.floyd_warshall()
		# self.print_graph()

	# compute all-pairs shortest path
	def floyd_warshall(self):
		n = self.num_nodes
		for k in range(n):
			for i in range(n):
				for j in range(n):
					self.A[i][j] = min(self.A[i][j], self.A[i][k] + self.A[k][j])

	def print_graph(self):
		for i in range(self.num_nodes):
			print(self.A[i])