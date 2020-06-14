# Monte Carlo Tree Search - Frozen Lake
Implementation of Monte Carlo Tree Search algorithm for solving the frozen lake problem.

## Monte Carlo Tree Search

Monte Carlo tree search (MCTS) is a heuristic search algorithm for some kinds of decision processes, most notably those employed in game play. The focus of MCTS is on the analysis of the most promising moves, expanding the search tree based on random sampling of the search space. The application of Monte Carlo tree search in games is based on many playouts, also called roll-outs. In each playout, the game is played out to the very end by selecting moves at random. The final game result of each playout is then used to weight the nodes in the game tree so that better nodes are more likely to be chosen in future playouts.

Source: [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)

This implementation uses UCT formula for searching the tree and balancing exploration and exploitation.

## The Frozen Lake

The frozen lake is a 4×4 grid with four possible types of areas  — safe (S), frozen (F), hole (H) and goal (G). The objective is to get from S to G avoiding all holes. In this implementation the agent (Monte Carlo Tree Search) is able to move through holes, however it receives negative points for each hole on it's path and positive points for each safe area, extra points are given for reaching G. Agent is also punished for path that is longer than 7 steps, as this is the shortest way to get from S to G. Script generates random frozen lake each time it is launched.

## Requirements

- Python 3.7
- numpy 1.18.1

## To do

- Some kind of cool tree visualization
- Tuning of UCT paramaters
- Other search methods than UCT
- Alllowing to perform another search on the same tree to check performance improvement
