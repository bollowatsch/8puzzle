import random
from copy import deepcopy

from exceptions import GridException
from heuristics import Heuristic, Hamming, Manhattan


class Node:
    """
    Basic Node class for a 3x3 grid of tiles (int). It contains the numbers 1 to 8 and None as a placeholder for an
    empty cell.
    """

    def __init__(self, initial_grid: list[int] = None, goal_state: list[int] = None, level: int = None,
                 f_val: int = None):
        self.grid = initial_grid if initial_grid is not None else self.create_random_grid()
        self.goal_state = goal_state if goal_state is not None else [None, 1, 2, 3, 4, 5, 6, 7, 8]
        self.level = 0 if level is None else level + 1
        self.f_val = f_val

        # Validate initial state
        if len(self.grid) != 9:
            raise GridException(f"Invalid grid size. The grid should be 9 tiles large, not {len(self.grid)}")
        for num in range(1, 9):
            if not self.grid.__contains__(num):
                raise GridException(f"The provided grid doesn't contain the number {num}."
                                    "A valid grid needs to hold each value form 1-8 exactly once.")
        if not self.grid.__contains__(None):
            raise GridException("The provided grid has no empty tile with value 'None'")
        if not self._is_solvable():
            raise GridException("The provided grid is not solvable.")

    def __eq__(self, other):
        # TODO equality is not enough, since we need to check, that the minimal cost of the state has to be saved
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.grid == other.grid

    def _is_solvable(self) -> bool:
        """8-puzzle is solvable if it contains an even number of misplaced tiles"""
        return self.number_of_misplaced_tiles() % 2 == 0

    def _is_goal_state(self) -> bool:
        """Compare grid to goal state."""
        return self.grid == self.goal_state

    def number_of_misplaced_tiles(self) -> int:
        """Count the number of misplaced tiles. Necessary for solvability as well as heuristics."""
        num: int = 0
        for i in range(9):
            if self.grid[i] != self.goal_state[i]:
                num += 1
        return num

    def _swap_tiles(self, i: int, j: int):
        """Swaps two tiles with corresponding indices."""
        self.grid[i], self.grid[j] = self.grid[j], self.grid[i]

    def _get_next_nodes(self) -> list:
        """
        Calculate all possible followup states, by swapping with the tile above (-3 tiles), left (-1 tile),
        right(+1 tile) and below (+3 tiles) from it.
        """
        # TODO there surely is a nicer way to do this...
        neighbor_offset = {
            0: [1, 3],
            1: [-1, 1, 3],
            2: [-1, 3],
            3: [-3, 1, 3],
            4: [-3, -1, 1, 3],
            5: [-3, -1, 3],
            6: [-3, 1],
            7: [-3, -1, 1],
            8: [-3, -1],
        }
        next_nodes: list[Node] = []
        empty_tile_index = self.grid.index(None)
        for offset in neighbor_offset[empty_tile_index]:
            temp_node = deepcopy(self)
            temp_node._swap_tiles(empty_tile_index, empty_tile_index + offset)
            next_nodes.append(temp_node)
        return next_nodes

    def get_level(self):
        return self.level

    @staticmethod
    def create_random_grid():
        grid: list[int] = [None, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(grid)
        return grid


class PuzzleSolver:
    def __init__(self, initial_grid: list[int], goal_state: list[int], heuristic: Heuristic):
        self.initial_grid = initial_grid
        self.goal_state = goal_state
        self.heuristic = heuristic
        self.explored_nodes = []

    def f_val(self, node: Node) -> int:
        """Returns total cost, consisting of actual cost and possible heuristic cost."""
        return node.get_level() + self.h_val(node)

    def g_val(self, node: Node) -> int:
        """Get current cost as number of iterations."""
        return node.get_level()

    def h_val(self, node: Node) -> int:
        """Get cost as calculated by chosen heuristic."""
        return self.heuristic.calc_heuristic_cost(node)
