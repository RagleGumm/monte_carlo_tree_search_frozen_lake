"""Contains classes/functions used for creation of game objects."""

from random import randint


class FrozenLakeCreator:
    """
    Creates frozen lake in the form of a list with holes and crossable path.
    The frozen lake is a 4x4 grid with 4 possible types of areas:
        — safe (S),
        - frozen (F),
        - hole (H),
        - goal (G).

    Attributes:
        positions_for_right_movement: list of positions after which
            right movement should be made
        positions_for_down_movement: list of positions after which
            down movement should be made
    """

    def __init__(self):
        self.positions_for_right_movement = [
            [1, 0],
            [2, 0],
            [3, 0],
            [3, 1],
            [3, 1],
            [3, 2],
        ]
        self.positions_for_down_movement = [[0, 3], [1, 3], [2, 3]]

    def move_through_lake(self, direction: str, position: list) -> list:
        """
        Calculates current position based on direction for movement.

        Args:
            direction: describes movement across the lake, 4 possibilities:
                - left
                - right
                - up
                - down
            position: 2 element list with row & column coordinates
                describing position on the frozen lake

        Returns:
            position: 2 element list with row & column coordinates
                describing new position on the frozen lake
        """
        if direction == "right":
            position[1] += 1
        elif direction == "left":
            position[1] -= 1
        elif direction == "up":
            position[0] -= 1
        elif direction == "down":
            position[0] += 1

        return position

    def create_crossable_path(self) -> list:
        """
        Creates crossable path across the frozen lake.
        Path has to start in [0, 0] and end in [3, 3].

        Returns:
            path: list of positions used to cross the lake
        """
        path = []
        position = [0, 0]
        path.append([0, 0])

        while not position == [3, 3]:
            if position in self.positions_for_right_movement:
                position = self.move_through_lake(
                    direction="right",
                    position=position
                )
                path.append(position.copy())
            elif position in self.positions_for_down_movement:
                position = self.move_through_lake(
                    direction="down",
                    position=position
                )
                path.append(position.copy())
            else:
                possible_movements = ["down", "right"]
                selected_direction = possible_movements[randint(0, 1)]
                position = self.move_through_lake(
                    direction=selected_direction, position=position
                )
                path.append(position.copy())

        return path

    def create_frozen_lake(self) -> list:
        """
        Creates frozen lake in the form of a list
        with holes and crossable path.

        Returns:
            frozen_lake: frozen lake in the form of a list with holes
                and crossable path
        """
        frozen_lake = [
            ["S", "F", "F", "F"],
            ["F", "F", "F", "F"],
            ["F", "F", "F", "F"],
            ["F", "F", "F", "G"],
        ]

        path = self.create_crossable_path()

        list_of_holes = []
        while len(list_of_holes) < 5:
            random_posistion = [randint(0, 3), randint(0, 3)]
            if (
                random_posistion not in path
                and random_posistion not in list_of_holes
            ):
                list_of_holes.append(random_posistion)

        for hole in list_of_holes:
            hole_row = hole[0]
            hole_column = hole[1]
            frozen_lake[hole_row][hole_column] = "H"

        return frozen_lake
