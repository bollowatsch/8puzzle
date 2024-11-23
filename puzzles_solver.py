from heuristics import manhattan, hamming


class PuzzleSolver:
    def get_f(self) -> int: #TODO implementation
        """Returns total cost, consisting of actual cost and possible heuristic cost."""
        return self.get_g() + self.get_h()

    def get_g(self) -> int: #TODO implementation
        """Get current cost as number of iterations."""
        pass

    def get_h(self) -> int: #TODO implementation
        """Get cost as calculated by chosen heuristic."""
        pass


class Node:
    """
    Basic Node class for a 3x3 grid of tiles (int). It contains the numbers 1 to 8 and None as a placeholder for an
    empty cell.
    """
    grid: list[int] = []
    _goal_state: list[int] = []

    def __init__(self, initial_grid=None, goal_state=None):
        self.grid = initial_grid if initial_grid is not None else [7, 2, 4, 5, None, 6, 8, 3, 1]
        self._goal_state = goal_state if goal_state is not None else [None, 1, 2, 3, 4, 5, 6, 7, 8]

        # Validate initial state
        if len(self.grid) != 9:
            raise Exception #TODO Exceptionclasses
        for num in range(1, 9):
            if not self.grid.__contains__(num):
                raise Exception  #TODO Exceptionclasses
        if not self.grid.__contains__(None):
            raise Exception #TODO Exceptionclasses
        if not self._is_solvable():
            raise Exception #TODO Exceptionclasses

    def _is_solvable(self) -> bool:
        """8-puzzle is solvable if it contians an even number of misplaced tiles"""
        return self._number_of_misplaced_tiles() % 2 == 0

    def _is_goal_state(self) -> bool:
        """Compare grid to goal state."""
        return self.grid == self._goal_state

    def _number_of_misplaced_tiles(self) -> int:
        """Count the number of misplaced tiles. Necessary for solvability as well as heurisitics."""
        num: int = 0
        for i in range(9):
            if self.grid[i] != self._goal_state[i]:
                num += 1
        return num

    def _swap_tiles(self, i:int, j:int):
        """Swaps two tiles with corresponding indices."""

    def _get_next_states(self) -> list:
        """Calculate all possible followup states."""
        next_nodes: list[Node] = []
        # index 0,2,6,8 -> 2 new possible states
        # index 1,3,5,7 -> 3 new possible states
        # index 4 -> 4 new possible states
        if self.grid[4] is None:
            # Swap with upper neighbour
            node1 = Node(self.grid)
            node1._swap_tiles(4,1)
            # Swap with left neighbor
            node2 = Node(self.grid)
            node2._swap_tiles(4, 3)
            # Swap with right neighbor
            node3 = Node(self.grid)
            node3._swap_tiles(4, 5)
            # Swap with down neighbor
            node4 = Node(self.grid)
            node4._swap_tiles(4, 7)

            next_nodes.extend([node1, node2, node3, node4])

        if self.grid[0] is None:
            # Swap with upper neighbour
            node1 = Node(self.grid)
            node1._swap_tiles(4,1)
            # Swap with left neighbor
            node2 = Node(self.grid)
            node2._swap_tiles(4, 3)
            # Swap with right neighbor
            node3 = Node(self.grid)
            node3._swap_tiles(4, 5)
            # Swap with down neighbor
            node4 = Node(self.grid)
            node4._swap_tiles(4, 7)

            next_nodes.extend([node1, node2, node3, node4])

        return next_nodes