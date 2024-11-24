"""
Module with all applicable heuristics for the 8-puzzle
"""
from abc import abstractmethod, ABC
from puzzles_solver import Node


class Heuristic:
    @abstractmethod
    def calc_heuristic_cost(self, node: Node):
        pass


class Manhattan(Heuristic):
    """calculates the sum of the distance each tile is from its goal position."""
    def calc_heuristic_cost(self, node: Node):
        sum = 0
        for num in node.grid:
            sum += abs(node.grid.index(num) - node.goal_state.index(num))
        return sum


class Hamming(Heuristic):
    """calculate the number of misplaced tiles."""
    def calc_heuristic_cost(self, node: Node):
        return node.number_of_misplaced_tiles()
