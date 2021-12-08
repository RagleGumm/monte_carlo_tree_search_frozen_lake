"""
Contains search policy functions used for finding best action.
Functions have to return str name of selected action.
"""

import math


def ucb_score(parent) -> str:
    """
    Calculates upper confidence bound for each child of a certain parent node.

    Args:
        parent - dict representing certain node of Monte Carlo tree

    Returns:
        best_action - string representing best action
    """
    ucb_scores = []

    for child in parent["child_nodes"].values():
        if child["visits"] == 0:
            ucb_scores.append(math.inf)
        else:
            exploitation_param = parent["reward"] / parent["visits"]
            exploration_param = math.sqrt(2)
            sqrt = math.sqrt(math.log(parent["visits"]) / child["visits"])
            ucb = exploitation_param + (exploration_param * sqrt)
            ucb_scores.append(ucb)

    max_score_index = ucb_scores.index(max(ucb_scores))
    all_actions = list(parent["child_nodes"].keys())
    best_action = all_actions[max_score_index]

    return best_action
