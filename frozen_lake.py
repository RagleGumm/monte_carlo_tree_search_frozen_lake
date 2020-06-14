# import dependencies
import math
from os import system, name
import numpy as np

# all possible movements across the lake
actions = {
    "up": np.array([-1, 0]),
    "down": np.array([1, 0]),
    "left": np.array([0, -1]),
    "right": np.array([0, 1]),
}


def clear_screen():
    """Clear screen depending on OS."""
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def choose_action(position):
    """Return list of actions based on current position.
    Used for creation of random frozen lake with crossable path.

    Parameters
    ----------
    position : np.array with x, y coordinates
    """
    if (
        np.array_equal(position, np.array([1, 0]))
        or np.array_equal(position, np.array([2, 0]))
        or np.array_equal(position, np.array([3, 0]))
        or np.array_equal(position, np.array([3, 1]))
        or np.array_equal(position, np.array([3, 2]))
    ):
        selected_actions = ["right"]
    elif (
        np.array_equal(position, np.array([0, 3]))
        or np.array_equal(position, np.array([1, 3]))
        or np.array_equal(position, np.array([2, 3]))
    ):
        selected_actions = ["down"]
    else:
        selected_actions = ["down", "right"]

    return selected_actions


def create_lake():
    """Returns random lake with holes
    and crossable path in the form of a list.
    """
    initial_lake = [
        ["S", "F", "F", "F"],
        ["F", "F", "F", "F"],
        ["F", "F", "F", "F"],
        ["F", "F", "F", "G"],
    ]

    position = np.array([0, 0])
    path = [np.array([0, 0])]

    while not np.array_equal(path[-1], np.array([3, 3])):
        selected_actions = choose_action(position)
        if len(selected_actions) > 1:
            action = selected_actions[np.random.randint(0, 2)]
            position = position + actions[action]
            path.append(position)
        else:
            action = selected_actions[0]
            position = position + actions[action]
            path.append(position)

    path = [x.tolist() for x in path]

    list_of_holes = []
    while len(list_of_holes) < 5:
        rand_pos = [np.random.randint(0, 4), np.random.randint(0, 4)]
        if rand_pos not in path and rand_pos not in list_of_holes:
            list_of_holes.append(rand_pos)

    for hole in list_of_holes:
        initial_lake[hole[0]][hole[1]] = "H"

    return initial_lake


def create_children(parent, selected_actions, actions):
    """Returns list of children for a certain parent node.

    Parameters
    ----------
    parent : dict representing certain node of monte carlo tree
    selected_actions : list of all possible actions (movements)
    actions : dict with all possible movements, global variable
    """
    children = []
    for action in selected_actions:
        child = {
            "position": parent["position"] + actions[action],
            "visits": 0,
            "reward": 0,
            "children": [],
        }

        children.append(child)

    return children


def create_tree(actions):
    """Creates root of the monte carlo tree and then adds children to the root.
    Returns tree in the form of a dictionary.

    Parameters
    ----------
    actions : dict with all possible movements, global variable
    """
    tree = {
        "position": np.array([0, 0]),
        "visits": 0, "reward": 0, "children": []
    }
    tree["children"] = create_children(tree, ["down", "right"], actions)

    return tree


def expand_tree(parent):
    """Expands certain node of the Monte Carlo tree
    according to available movements.

    Parameters
    ----------
    parent : dict representing certain node of Monte Carlo tree
    """
    # corners
    if np.array_equal(parent["position"], np.array([0, 0])):
        selected_actions = ["down", "right"]
        parent["children"] = create_children(parent, selected_actions, actions)
    elif np.array_equal(parent["position"], np.array([0, 3])):
        selected_actions = ["down", "left"]
        parent["children"] = create_children(parent, selected_actions, actions)
    elif np.array_equal(parent["position"], np.array([3, 0])):
        selected_actions = ["up", "right"]
        parent["children"] = create_children(parent, selected_actions, actions)
    elif np.array_equal(parent["position"], np.array([3, 3])):
        selected_actions = ["up", "left"]
        parent["children"] = create_children(parent, selected_actions, actions)
    # edges excluding corners
    elif (
        np.array_equal(parent["position"], np.array([0, 1]))
        or np.array_equal(parent["position"], np.array([0, 2]))
    ):
        selected_actions = ["down", "left", "right"]
        parent["children"] = create_children(parent, selected_actions, actions)
    elif (
        np.array_equal(parent["position"], np.array([3, 1]))
        or np.array_equal(parent["position"], np.array([3, 2]))
    ):
        selected_actions = ["up", "left", "right"]
        parent["children"] = create_children(parent, selected_actions, actions)
    elif (
        np.array_equal(parent["position"], np.array([1, 0]))
        or np.array_equal(parent["position"], np.array([2, 0]))
    ):
        selected_actions = ["down", "up", "right"]
        parent["children"] = create_children(parent, selected_actions, actions)
    elif (
        np.array_equal(parent["position"], np.array([1, 3]))
        or np.array_equal(parent["position"], np.array([2, 3]))
    ):
        selected_actions = ["down", "up", "left"]
        parent["children"] = create_children(parent, selected_actions, actions)
    # middle fields
    else:
        selected_actions = ["up", "down", "left", "right"]
        parent["children"] = create_children(parent, selected_actions, actions)


def ucb_score(parent):
    """Calculates upper confidence bound for each child of a certain parent node.
    Returns index (integer) of a child to be selected
    from parent['children'] list.

    Parameters
    ----------
    parent : dict representing certain node of Monte Carlo tree
    """
    ucb_scores = []
    for child in parent["children"]:
        if child["visits"] == 0:
            ucb_scores.append(math.inf)
        else:
            exploit = parent["reward"] / parent["visits"]
            explore = np.sqrt(2)
            sqrt = np.sqrt(np.log(parent["visits"]) / child["visits"])
            ucb = (exploit + (explore * sqrt))
            ucb_scores.append(ucb)
    return ucb_scores.index(max(ucb_scores))


def calculate_reward(path):
    """Calculates reward for certain path according to the following rules:
    - S and F are rewarded 1 point,
    - G is rewarded 2 points,
    - H is rewarded 2 negative points,
    - path longer than 7 steps receives 2 negative for each additional step.

    Returns sum of rewards as integer.

    Parameters
    ----------
    path : list of letters corresponding to selected path
    """
    reward_sum = 0
    if len(path) > 7:
        reward_sum -= (len(path) - 7) * 2

    for step in path:
        if step in ("S", "F"):
            reward_sum += 1
        elif step == "G":
            reward_sum += 2
        else:
            reward_sum -= 2
    return reward_sum


def backpropagation(tree, reward, positions):
    """Update information (reward, visits) in the tree nodes
    corresponding to selected path.

    Parameters
    ----------
    tree : dict, instance of Monte Carlo tree
    reward : int, reward for ceratin path, output of calculate_reward
    positions: list of poisitions (np.arrays) corresponding to selected path
    """
    tree["reward"] += reward
    tree["visits"] += 1
    node = tree
    while len(positions) > 0:
        for child in node["children"]:
            if np.array_equal(positions[0], child["position"]):
                node = child
                node["reward"] += reward
                node["visits"] += 1
        positions = positions[1:]


def explore_tree(tree, lake):
    """One round of Monte Carlo Tree Search including
    selection, expansion, simulation and backpropagation phase.
    Returns list of letters (path) and np.arrays (positions)
    corresponding to selected path.

    Parameters
    ----------
    tree - dict, instance of the Monte Carlo tree
    lake - list, randomly created frozen lake
    """
    # initialize variables
    current = tree
    path = []
    positions = []
    path.append(lake[current["position"][0]][current["position"][1]])
    positions.append(current["position"])

    # selection until child nodes exist
    # update path and positions after each iteration
    while current["children"]:
        best_action = ucb_score(current)
        current = current["children"][best_action]
        path.append(lake[current["position"][0]][current["position"][1]])
        positions.append(current["position"])
    # no child nodes
    else:
        # current node has not been visited yet
        # simulation and backpropagation
        if current["visits"] == 0:
            reward = calculate_reward(path)
            backpropagation(tree, reward, positions)
        # current node has been visited
        # expansion, selection of first available child
        # simulation and backpropagation
        else:
            expand_tree(current)
            current = current["children"][0]
            reward = calculate_reward(path)
            backpropagation(tree, reward, positions)

    return path, positions


def print_results(path, positions, counter):
    """Prints out the results of each round of Monte Carlo Tree Search.

    Parameters
    ----------
    path : list of letters corresponding to selected path
    positions: list of poisitions (np.arrays) corresponding to selected path
    counter : int, counts iterations
    """
    empty_lake = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."],
    ]

    reward = calculate_reward(path)
    for x in range(len(positions)):
        empty_lake[positions[x][0]][positions[x][1]] = path[x]

    print("---Iteration {}---\n".format(counter))

    for x in range(4):
        print(
            frozen_lake[x][0],
            frozen_lake[x][1],
            frozen_lake[x][2],
            frozen_lake[x][3],
            "    ",
            empty_lake[x][0],
            empty_lake[x][1],
            empty_lake[x][2],
            empty_lake[x][3],
        )

    print("\nSteps: {}".format(len(path)))
    print("Reward: {}\n\n".format(reward))


def find_path(tree, lake):
    """Performs Monte Carlo Tree Search until safe path is found.

    Parameters
    ----------
    tree - dict, instance of the Monte Carlo tree
    lake - list, randomly created frozen lake
    """
    counter = 1
    while True:
        selected_path, selected_positions = explore_tree(tree, lake)
        print_results(selected_path, selected_positions, counter)
        counter += 1
        if "G" in selected_path and "H" not in selected_path:
            break


if __name__ == "__main__":
    # create root of monte carlo tree and add children
    mcts_tree = create_tree(actions)

    # random creation of frozen lake
    frozen_lake = create_lake()

    # clear screen, print intro
    clear_screen()
    print("So, here's our frozen lake:\n")
    for line in frozen_lake:
        print(line[0], line[1], line[2], line[3])
    print("\nS: starting point, safe")
    print("F: frozen surface, safe")
    print("H: hole, fall to your doom")
    print("G: goal\n")
    print("The goal is to get from S to G avoiding all H.")
    print("Now let's see how Monte Carlo Tree Search can deal with that.\n")
    input("Press Enter to continue.")
    print("\n\n")
    # find path through the lake
    find_path(mcts_tree, frozen_lake)

    # whether to continue with another random lake
    while True:
        continuation = input("Create another lake[y/n]?")
        if continuation == "y":
            mcts_tree = create_tree(actions)
            frozen_lake = create_lake()
            find_path(mcts_tree, frozen_lake)
        else:
            break
