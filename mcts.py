"""Contains MonteCarloTreeSearch class used for sovling of optimization problems."""

from action_policy import ActionPolicy
from reward_policy import RewardPolicy


class MonteCarloTreeSearch:
    """
    Finds solution to given optimization problem using
    Monte Carlo Tree Search algorithm.

    Attributes:
        search_policy: function used for selection of best action
        action_policy: class used for establishing possible actions & modyfying
            node state according to selected action
        reward_policy: class used for calculation of reward
            & checking if end condition was reached
        exploration_counter: counter of tree exploration runs
        solution: solution of the optimization problem
        root: root node of the Monte Carlo tree
    """

    def __init__(
        self,
        search_policy: callable,
        action_policy: ActionPolicy,
        reward_policy: RewardPolicy,
        root_state,
    ):
        """
        Sets attributes when instance is created.

        Args:
           root_state: state to be assigned to root of the tree
        """
        self.search_policy = search_policy
        self.action_policy = action_policy
        self.reward_policy = reward_policy
        self.exploration_counter = 0
        self.solution = None

        # create root
        self.root = {
            "state": root_state,
            "visits": 0,
            "reward": 0,
            "child_nodes": {},
        }

        # add children to root according to possible actions
        possible_actions = self.action_policy.establish_possible_actions(
            self.root
        )
        self.create_child_nodes_for_current_node(
            possible_actions=possible_actions, current_node=self.root
        )

    def create_child_nodes_for_current_node(
        self, possible_actions: list, current_node: dict
    ):
        """
        Adds children nodes to current node.

        Args:
            selected_actions: list of all possible actions
            current_node: dict representing certain node of monte carlo tree
        """
        for action in possible_actions:
            parent_state = current_node["state"].copy()
            child_state = self.action_policy.modify_state_according_to_action(
                state=parent_state, action=action
            )
            child = {
                "state": child_state,
                "visits": 0,
                "reward": 0,
                "child_nodes": {},
            }
            current_node["child_nodes"][action] = child

    def backpropagation(self, reward: int, move_sequence: dict):
        """
        Updates information (reward, visits) in the tree nodes
        corresponding to selected move sequence.

        Args:
            reward: reward for certain move sequence
            move_sequence: keys are states & actions,
                values are lists of states & actions from exploration phase
        """
        self.root["reward"] += reward
        self.root["visits"] += 1
        current_node = self.root

        all_actions = move_sequence["actions"]
        while len(all_actions) > 0:
            selected_action = all_actions[0]
            current_node = current_node["child_nodes"][selected_action]
            current_node["reward"] += reward
            current_node["visits"] += 1
            all_actions = all_actions[1:]

    def explore_tree(self) -> dict:
        """
        One round of Monte Carlo Tree Search including
        selection, expansion, simulation and backpropagation phase.

        Returns:
            move_sequence: keys are states & actions,
                values are lists of states & actions from exploration phase
        """
        # initialize variables
        move_sequence = {"states": [], "actions": []}
        current_node = self.root
        move_sequence["states"].append(current_node["state"].copy())

        # selection until child nodes exist
        # update move_sequence each iteration
        while current_node["child_nodes"]:
            best_action = self.search_policy(current_node)
            selected_node = current_node["child_nodes"][best_action]
            current_node = selected_node
            move_sequence["states"].append(current_node["state"].copy())
            move_sequence["actions"].append(best_action)
        # no child nodes
        else:
            # current node has not been visited yet
            # simulation and backpropagation
            if current_node["visits"] == 0:
                reward = self.reward_policy.calculate_reward(move_sequence)
                self.backpropagation(
                    reward=reward,
                    move_sequence=move_sequence
                )
            # current node has been visited
            # expansion, selection of first available child
            # simulation and backpropagation
            else:
                possible_actions = self.action_policy.establish_possible_actions(
                    current_node
                )
                self.create_child_nodes_for_current_node(
                    possible_actions=possible_actions,
                    current_node=current_node
                )
                first_action = possible_actions[0]
                selected_node = current_node["child_nodes"][first_action]
                current_node = selected_node
                reward = self.reward_policy.calculate_reward(move_sequence)
                self.backpropagation(
                    reward=reward,
                    move_sequence=move_sequence
                )

        return move_sequence

    def find_solution(self):
        """Explores the tree until solution is found."""
        end_condition = False
        while not end_condition:
            move_sequence = self.explore_tree()
            self.exploration_counter += 1
            end_condition = self.reward_policy.check_end_condition(
                move_sequence
            )

        self.solution = move_sequence
