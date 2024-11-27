"""
Module with all applicable heuristics for the 8-puzzle
"""
from abc import abstractmethod



class Heuristic:
    @abstractmethod
    def calc_heuristic_cost(self, grid: list[int], goal_state: list[int]):
        pass


class Manhattan(Heuristic):
    """calculates the sum of the distance each tile is from its goal position."""
    def calc_heuristic_cost(self, grid: list[int], goal_state: list[int]) -> int:
        sum = 0
        size = int(len(grid) ** 0.5)
        for num, tile in enumerate(grid):

            # exclude empty tile
            if tile is None:
                continue

            # Current position (row, col)
            curr_row, curr_col = divmod(num, size)

            # Goal position (row, col)
            goal_index = goal_state.index(tile)
            goal_row, goal_col = divmod(goal_index, size)

            sum += abs(curr_row - goal_row) + abs(curr_col - goal_col)
            # print("Calculated Manhattan costs:" + str(sum))
        return sum


class Hamming(Heuristic):
    """calculate the number of misplaced tiles."""
    def calc_heuristic_cost(self,grid: list[int], goal_state: list[int]) -> int:
        count = 0
        for i in range(len(grid)):
            if grid[i] is not None and grid[i] != goal_state[i]:
                count += 1
        return count
