"""
Module with all applicable heuristics for the 8-puzzle
"""
from abc import abstractmethod
from puzzles_solver import Node


class Heuristic:
    @abstractmethod
    def calc_heuristic_cost(self, node: Node):
        pass


class Manhattan(Heuristic):
    """calculates the sum of the distance each tile is from its goal position."""
    def calc_heuristic_cost(self, node: Node):
        sum = 0
        size = int(len(node.grid) ** 0.5)
        for num, tile in node.grid:

            # exclude empty tile
            if tile is None:
                continue

            # Current position (row, col)
            curr_row, curr_col = divmod(num, size)

            # Goal position (row, col)
            goal_index = node.goal_state.index(num)
            goal_row, goal_col = divmod(goal_index, size)

            sum += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return sum


class Hamming(Heuristic):
    """calculate the number of misplaced tiles."""
    def calc_heuristic_cost(self, node: Node):
        return node.number_of_misplaced_tiles()
