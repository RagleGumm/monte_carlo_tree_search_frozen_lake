"""
Contains ActionPolicy classes used for establishing possible actions
based on given node state & modification of node state
according to selected action.
"""

from abc import ABC, abstractmethod


class ActionPolicy(ABC):
    @abstractmethod
    def modify_state_according_to_action(self, state, action: str):
        """
        Modifies node state according to selected action.
        Returns modified state.
        """
        pass

    @abstractmethod
    def establish_possible_actions(self, current_node: dict):
        """
        Establishes possible actions based on state of given node.
        Returns list of possible actions (str).
        """
        pass


class FrozenLakeActionPolicy(ActionPolicy):
    """
    Established possible movementes across frozen lake
    according to current position.
    Modifies position according to selected action.
    """

    def modify_state_according_to_action(
        self, state: list, action: str
    ) -> list:
        """
        Calculates current position based on direction for movement.

        Args:
            state: current position on the lake
            action: describes movement across the lake, 4 possibilities:
                - left
                - right
                - up
                - down
        """
        if action == "right":
            state[1] += 1
        elif action == "left":
            state[1] -= 1
        elif action == "up":
            state[0] -= 1
        elif action == "down":
            state[0] += 1

        return state

    def establish_possible_actions(self, current_node: dict) -> list:
        """
        Establishes possible actions based on current position on the lake.

        Args:
            current_node: node based on which possible actions are established

        Returns:
            possbile_actions: list of possible actions
        """
        possible_actions = []

        row_position = current_node["state"][0]
        column_position = current_node["state"][1]

        if row_position in [1, 2]:
            possible_actions.extend(["up", "down"])
        elif row_position == 0:
            possible_actions.append("down")
        elif row_position == 3:
            possible_actions.append("up")

        if column_position in [1, 2]:
            possible_actions.extend(["left", "right"])
        elif column_position == 0:
            possible_actions.append("right")
        elif column_position == 3:
            possible_actions.append("left")

        return possible_actions
