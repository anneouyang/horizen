# Horizen
A simulation of how the blockchain network behaves under different conditions with [Horizen's proposal](https://www.horizen.global/assets/files/A-Penalty-System-for-Delayed-Block-Submission-by-Horizen.pdf) -- a modified Satoshi consensus using a penalty system for delayed block submission to enhance protection against 51% attacks. 



## [Model 1](/model_1)

This is an ideal situation:

- There are no network delays:
  - Every block gets processed as soon as the node submits the block to the blockchain
  - Every node always sees the most updated version of the blockchain
- Nodes are behaving consistently:
  - Honest nodes are always honest
  - Malicious nodes are mining their own chain and trying to overtake the main chain through a 51% attack

**Result**: The protocol appears to be working in the way it is described, and a chain split has not been observed.



## [Model 2](/model_2)

Removing the guarantee of no network delays:

- Assume that all nodes are behaving honestly
- Due to network delays, nodes might be adding "old blocks" to the main chain with a non-malicious intent, and these blocks have penalty associated with them

**Implementation Assumptions**: Organize the nodes into a network where the propagation of information along different edges takes an varying amount of time (determined randomly from a range), and nodes always send and receive information along the fastest routes (shortest paths). Essentially, in this model, the nodes don't always receive the most up-to-date information about the main chain.

**Result**: The protocol appears to be working in the way it is described without chain splits, and the height of the main chain grows linearly with time:

![](/model_2/res/time_height.png)



## Model 3

There's one attempt at chain reorganization



## Model 4

There are multiple attempts at chain reorganization



## Model 5

There are sporadic disconnections in the network