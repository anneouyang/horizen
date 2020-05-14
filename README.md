# Simulating Horizen's Penalty System for Delayed Block Submission

## Introduction

A double-spending can occur when a node or a group of nodes control more than 51% of the network's total hashing power. To perform a double-spending attack, the malicious node commits a transaction initially and begins to secretly mine a private chain without including that transaction. After the initial transaction has enough confirmations, the malicious node releases the private chain in which the transaction never occurred to reverse the transaction. Since the malicious node has more hashing power than the rest of the network combined, it is able to mine faster and the private chain, which is longer and has more work associated with it, will cause the rest of the network to agree on the fraudulent branch. In this scenario, the initial transaction is voided although the attacker has already received the product, so the attacker has the coins back and can spend them again. 



[Horizen's proposal](https://www.horizen.global/assets/files/A-Penalty-System-for-Delayed-Block-Submission-by-Horizen.pdf) increases the difficulty of successfully executing this attack by incurring "a penalty in the form of a block acceptance delay in relation to the amount of time the block has been hidden from the public network". Time here is measured in block intervals and the penalty is applied based on the difference between the current main chain height (*m*) and the height of the received block (*h*). If *h > m*, the penalty is -1; otherwise the penalty is calculated using the delay function *DF = (m - h) \* f(d)*, where *f(d)* is a function that can be used to adjust the magnitude of the delay penalty. The chain will only be accepted when the penalty is zero — whether because the node always submits blocks in a timely manner or it has mined enough blocks to successfully drive the delayed penalty to zero by exceeding the main chain height by a lot.



This project is a python simulation of how the blockchain network behaves under different conditions with Horizen's proposal. Models simulating different scenarios are tested and various parameters are adjusted to reason about the network's behavior in different circumstances. 



## Modeling the System

The model has three main components:

1. The **blockchain** contains a record of all the blocks submitted by the nodes. In this implementation, this blockchain is shared by all the nodes but different subsets of blocks are visible to different nodes. Each node keeps track of the main chain based on its current view. 
2. The **network** contains all the nodes currently in the network and the pairwise time delay when communicating for all possible pairs of nodes. Transitive closure is used to guarantee that when a node wants to relay a message to another node, the path with the shortest time delay (not necessarily the path with the smallest number of nodes) is always used.
3. **Nodes** are the individual decision units in this network; they can generate blocks and commit blocks to the blockchain, and they can either act honestly or maliciously. In this model, each unit of time is some block interval (not temporal). Nodes have different hash rates, and the rate property of a node denotes how many blocks it can produce in a unit of time. 



## Results in Different Scenarios

### Case 1 - No delays, no attacks

This case is the ideal situation in which there are no network delays and nodes are always behaving honestly. More specifically, no network delays means that every block gets propagated to all the nodes in the network as soon as it is submitted by a node, and every node always sees the most updated version of the blockchain. An honest node always mines according to the set rules of the system and contributes to the functioning of the system — it doesn't try to deliberately cause a reorg and always mines on the current main chain. 

The results are represented in two graphs, the first graph shows the maximum percentage of nodes agreeing on some block as the head of the chain. For every possible head of the chain, the percentage is defined as the number of nodes recognizing it as a head of the chain divided by the total number of nodes. The second graph shows the number of distinct heads, which should be less than or equal to the total number of nodes. 

![Model 1 Picture 1](./res/m1p1.png)

As demonstrated by the results graphs, in this case there is only one distinct head which all the nodes agree on, so consensus can be reached and the protocol seems to be working as described. 



### Case 2 - Delays, no attacks

In this case, the guarantee of no network delays is removed, but all the nodes are still behaving honestly. The network delay in this model is implemented by delaying the time at which a particular block becomes visible to a node. For example, if the time delay of communication between node A and node B is *x* seconds, when A adds a block to the blockchain at time *t*, the block becomes visible to node B at time *x + t*. 

![m2p2](./res/m2p2.png)

The results show that if the delay is sufficiently high, a chain split may happen at first (there are 2 distinct heads and only a maximum of 20% of the nodes agree on some head). If given a long enough "wait period" in which no new blocks are being added to the blockchain, however, the nodes will eventually reach consensus. 



### Case 3 - One malicious party

In this case, there is a malicious party attempting to cause a chain reorg. This is implemented in the model by letting the attacker secretly mine a chain and submit after the block it is trying to undo has *x* number of blocks mined on top of it in the main chain (when it has received enough confirmations)

First, assume there's negligible network delay, in the case where the attacker has:

- <50% of the total computing power: 

  ![](./res/m3p1.png)

  The attacker cannot successfully cause a chain reorg. Eventually the rest of the network will reach consensus disregarding the attacker.

-  53% of the total computing power:

  ![](./res/m3p2.png)

  Initially all the nodes are in consensus. When the attacker publishes its secret chain, the rest of the network is still in consensus (90% of the nodes agree on a single head) disregarding this new chain. The attacker continues to mine on the new chain and eventually all the nodes will switch over to the attacker's chain when the penalty has been driven down to zero. 

-  68% of the total computing power:

  ![](./res/m3p3.png)

  The behavior is the exact same as the case where the attacker has 53% of the total computing power, except the reorg occurs faster because the more powerful attacker is able to drive the penalty down to zero faster. 

In the case there is significant network delay, the network may fail to reach consensus.

![](./res/m3p4.png)



### Case 4 - Multiple malicious parties

In this case there are multiple malicious nodes attempting at chain reorganization. Each individual group of attackers has more computing power than the total computing power of all the remaining honest nodes in the network (not including the other attackers)

![](./res/m4p1.png)

When there are no network delays, the group of nodes with the most computing power ends up dominating — causing the honest nodes to agree with it. Since the total hashing power of this successful attacker and all the honest nodes combined is greater than all the other attackers individually, the other groups will not be able to carry out an attack. If they continue to attack, they will be ignored by the rest of the network. 

![](./res/m4p2.png)

Similar to case 3, if there are network delays, the network may fail to reach consensus eventually.



### Case 5 - Merging disjoint networks

In this case, two parts of the network are initially disjoint. The attempt to merge them together after a certain amount of time has elapsed is not successful. Because of the large values of the delay penalties when each part sees the blocks of the other part, the nodes in the two parts of the network will continue to perform as if the merge never existed and never reach consensus. 

![](./res/m5p1.png)



## Adjusting Parameters

One parameter I adjusted is the attacker's hash rate (when there's only a single group of attackers and no network delay) to see how many units of time it would take the network to converge after releasing the secret chain (after a certain number of confirmations). The following table summarizes the results (N/A denotes the divergence of the network)

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

Note that the traditional consensus protocol always has a convergence time of 1 because the chain reorg happens as soon as the longer branch is published. This shows that the modified consensus protocol indeed makes an attack more expensive. An attacker either has to sustain a majority of the computing power for a longer period of time or need more computing power to reduce the time it needs to sustain. 



As mentioned before, the function *f(d)* in the delay function *DF = (m - h) \* f(d)* can be adjusted to change the magnitude of the penalty. In modeling all the cases above, *f(d)* is set to the constant *1*. In this part, I adjusted  the value of *f(d)* to be different constants. The following table, based on an attacker with 53% of the total hashrate of the network and there's no delay in the network, shows the relationship between the delay factor penalty and the average time to converge. Note that when the *f(d)=0* it is the same as the traditional Nakamoto consensus. 

| *f(d)*      | Average time to converge |
| ----------- | ------------------------ |
| 0           | 1                        |
| 1 (default) | 20                       |
| 2           | 37                       |
| 3           | 53                       |
| 4           | 70                       |

This shows that where there's negligible delay in the network, *f(d)* can be adjusted to effectively increase the cost of the attack. 



Consider the case when there's non-negligible delay in the network. Letting the delay penalty having a greater magnitude can reduce the tolerance for bad network conditions, making it harder for the nodes to reach consensus. 

| *f(d)*      | Approximate delay tolerance threshold |
| ----------- | ------------------------------------- |
| 0           | very high                             |
| 1 (default) | 10 - 15                               |
| 2           | 3 - 4                                 |
| 3           | 0                                     |
| 4           | 0                                     |



## Summary

Horizen's modified consensus can increase the cost of carrying out a double-spending attack; however, it comes with a tradeoff of decreased tolerance for bad network conditions. If the delays are high enough or if the network is separated for a certain period of time, the network may fail to reach consensus eventually. In order for this to happen, the delay needs to be on the order of magnitude of many "block intervals", which can be quite high when converted to temporal time. 



## Future Work

Although this model is able to show a few interesting observations, it is a simplified and contrived version of the real-world system. In the future, the model can be refined to become more closely aligned with the real-world implementation, and real data can be incorporated to perform more rigorous quantitative analysis regarding how much more expensive exactly it is to perform an attack, how much network delay (measured temporally) the network can tolerate without splitting, and what is the optimal *f(d)* to account for the tradeoff between making the network more resistant to attacks and more resistant to bad network conditions. 