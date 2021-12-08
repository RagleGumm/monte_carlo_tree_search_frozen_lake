"""
Contains RewardPolicy classes used for calcualtions of reward
& checking of search end condition.
"""

from abc import ABC, abstractmethod


class RewardPolicy(ABC):
    @abstractmethod
    def calculate_reward(self, move_sequence: dict) -> int:
        """
        Calculates reward for certain move sequence.
        Returns reward sum.
        """
        pass

    @abstractmethod
    def check_end_condition(self, move_sequence: dict) -> bool:
        """
        Checks if search end conditions has been reached
        based on move sequence.
        Returns True/False.
        """
        pass


class FrozenLakeRewardPolicy(RewardPolicy):
    """
    Calculates reward for certain path across frozen lake.
    Checks if crossable path has been found.
    """

    def __init__(self, game_object: list):
        """
        Sets attributes when instance is created.

        Args:
           game_object: frozen lake in the form of a list
        """
        self.game_object = game_object

    def calculate_reward(self, move_sequence: dict) -> int:
        """
        Calculates reward for certain path according to the following rules:
            - S and F are rewarded 1 point,
            - G is rewarded 2 points,
            - H is rewarded 2 negative points,
            - path longer than 7 steps receives 2 negative points
                for each additional step.

            Returns sum of rewards as integer.

        Args:
            move_sequence: keys are states & actions,
                values are lists of states & actions from exploration phase

        Returns:
            reward_sum: sum of reward
        """
        all_states = move_sequence["states"]
        path_across_lake = []
        for state in all_states:
            row_position = state[0]
            column_position = state[1]
            type_of_area = self.game_object[row_position][column_position]
            path_across_lake.append(type_of_area)

        reward_sum = 0
        if len(path_across_lake) > 7:
            reward_sum -= (len(path_across_lake) - 7) * 2

        for step in path_across_lake:
            if step in ("S", "F"):
                reward_sum += 1
            elif step == "G":
                reward_sum += 2
            else:
                reward_sum -= 2

        return reward_sum

    def check_end_condition(self, move_sequence: dict) -> bool:
        """
        Checks if game end condition has been reached.

        Args:
           move_sequence: keys are states & actions,
                values are lists of states & actions from exploration phase

        Returns:
            end_condition: True/False depending whether end condition
                was reached
        """
        all_states = move_sequence["states"]
        path_across_lake = []
        for state in all_states:
            row_position = state[0]
            column_position = state[1]
            type_of_area = self.game_object[row_position][column_position]
            path_across_lake.append(type_of_area)

        if "G" in path_across_lake and "H" not in path_across_lake:
            end_condition = True
        else:
            end_condition = False

        return end_condition
