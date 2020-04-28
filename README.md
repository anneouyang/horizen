# Horizen
This is a simulation of how the blockchain network behaves under different conditions with [Horizen's proposal](https://www.horizen.global/assets/files/A-Penalty-System-for-Delayed-Block-Submission-by-Horizen.pdf) -- a modified Satoshi consensus using a penalty system for delayed block submission to enhance protection against 51% attacks. 



## I: Behavior of the network under the protocol

### Model 1 - No delays no attacks

This is an ideal situation:

- There are no network delays:
  - Every block gets processed as soon as the node submits the block to the blockchain
  - Every node always sees the most updated version of the blockchain
- Nodes are behaving consistently:
  - Honest nodes are always honest
  - Malicious nodes are mining their own chain and trying to overtake the main chain through a 51% attack

**Result**: The protocol appears to be working in the way it is described, and a chain split has not been observed

![Model 1 Picture 1](./res/m1p1.png)



### Model 2 - Delays, no attacks

Removing the guarantee of no network delays:

- Assume that all nodes are behaving honestly
- Due to network delays, nodes might be adding "old blocks" to the main chain with a non-malicious intent, and these blocks have penalty associated with them

**Implementation Assumptions**: Organize the nodes into a network where the propagation of information along different edges takes an varying amount of time (determined randomly from a range), and nodes always send and receive information along the fastest routes (shortest paths). Essentially, in this model, the nodes don't always receive the most up-to-date information about the blocks being added to the chain.

**Result**: Even with delays, given a sufficiently long "wait period" where no new blocks are being added, the nodes will eventually "catch up" with the information and reach consensus:

![Model 2 Pic 1](./res/m2p1.png)

If the delay is sufficiently high, the blockchain may be very not converge at first; however, it will converge if given enough time for the network to settle (i.e. no new nodes are added to the blockchain)

![m2p2](./res/m2p2.png)



### Model 3 - One attacking group, delays and no delays

There's one malicious node attempting to cause a chain reorganization. 

First, assume there is negligible network delay; here are the cases where the attacker has:

- <50% of the total computing power:

  ![](./res/m3p1.png)

- 53% of the total computing power:

  ![](./res/m3p2.png)

- 68% of the total computing power:

  ![](./res/m3p3.png)

When there is significant network delay, the network may fail to reach consensus:

![](./res/m3p4.png)



### Model 4 - Multiple attacking groups, delays and no delays

There are multiple malicious nodes attempting at chain reorganization.

When there are no network delays, the group of nodes with the most computing power ends up dominating, and the other groups will have no choice but to agree with the reached consensus:

In this case, 3 groups of node are trying to launch attacks, and one ends up dominating:

![](./res/m4p1.png)

When there are network delays and multiple malicious nodes trying to launch 51% attacks, the network may fail to reach consensus eventually:

![](./res/m4p2.png)



### Model 5 - Merging two disjoint parts of the network

Initially, two parts of the networks are disjoint. The attempt to merge them together after a certain amount of time has elapsed is not successful. Because of the large values of the delay penalties, the nodes in the two parts of the network will continue to perform as if the merge never existed.

![](./res/m5p1.png)



## II: Comparison with the traditional Nakamoto consensus



### Convergence time for attacks with different hash rates

Time is defined in a way such that in each unit of time, all the nodes are able to produce a certain number of blocks corresponding to their hash rate. 

When there's one attacking group, assuming there's no network delay, the average time for the network to converge under the traditional and modified (with delay factor of 1) consensus protocols are summarized in the following table:

| Attacker Hashrate | Average time to converge (traditional) | Average time to converge (modified) |
| ----------------- | -------------------------------------- | ----------------------------------- |
| <50%              | N/A                                    | N/A                                 |
| 50%               | N/A                                    | N/A                                 |
| 53%               | 1                                      | 20                                  |
| 55%               | 1                                      | 10                                  |
| 57%               | 1                                      | 6                                   |
| 59%               | 1                                      | 5                                   |
| 61%               | 1                                      | 3                                   |
| 63%               | 1                                      | 3                                   |
| 64%               | 1                                      | 2                                   |
| 65%               | 1                                      | 2                                   |
| 67%               | 1                                      | 2                                   |
| 68%               | 1                                      | 1                                   |

Note that the traditional consensus protocol always has a convergence time of 1 because the chain reorg happens as soon as the longer branch is published.



### Delay factor penalty and convergence time in the presense of an attacker and no network delays

One way to increase the cost incurred on the attacker is to set the delay factor penalty to a higher value. The delay factor penalty is used to calculate the penalty. The following table, based on an attacker with **53%** of the total hashrate of the network, shows the relationship between the delay factor penalty and the average time to converge:

| Delay Factor penalty     | Average time to converge |
| ------------------------ | ------------------------ |
| 0 (traditional Nakamoto) | 1                        |
| 1 (default, minimum)     | 20                       |
| 2                        | 37                       |
| 3                        | 53                       |
| 4                        | 70                       |



### Delay factor penalty and convergence time in the presense of an attacker and network delays

Having a higher delay factor penalty, however, makes it harder for the network to converge in the presence of network delays, so a higher delay factor penalty can lead to lower tolerance for bad network conditions. 

| Delay Factor (penalty)   | Approximate delay tolerance threshold |
| ------------------------ | ------------------------------------- |
| 0 (traditional Nakamoto) | very high                             |
| 1 (default, minimum)     | 10 - 15                               |
| 2                        | 3 - 4                                 |
| 3                        | 0                                     |
| 4                        | 0                                     |

