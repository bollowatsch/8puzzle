from heuristics import manhattan, hamming


class Node:
    """
    Basic Node calss for a 3x3 grid of tiles (int). It contains the numbers 1 to 8 and None as a placeholder for an
    empty cell.
    """
    grid: list[int] = []
    _goal_state: list[int] = [None, 1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self, initial_grid=None):
        self.grid = initial_grid if initial_grid is not None else [7, 2, 4, 5, None, 6, 8, 3, 1]

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
