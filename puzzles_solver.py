import random
from copy import deepcopy
import heapq
import time
import statistics

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

        self.solvable = self._is_solvable()

    def __eq__(self, other):
        # TODO equality is not enough, since we need to check, that the minimal cost of the state has to be saved
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.grid == other.grid

    def _is_solvable(self) -> bool:
        """8-puzzle is solvable if it contains an even number of inversions"""
        inversions: int = 0
        n = len(self.grid)

        # Compare each tile with all tiles after it
        for i in range(n):
            for j in range(i + 1, n):
                if self.grid[i] is not None and self.grid[j] is not None:
                    if self.grid[i] > self.grid[j]:
                        inversions += 1

        return inversions % 2 == 0

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

    def __lt__(self, other):
        """Define comparison for Node based on level."""
        return self.level < other.level

    def _swap_tiles(self, i: int, j: int):
        """Swaps two tiles with corresponding indices."""
        self.grid[i], self.grid[j] = self.grid[j], self.grid[i]

    def _get_next_nodes(self) -> list:
        """
        Calculate all possible followup states, by swapping with the tile above (-3 tiles), left (-1 tile),
        right(+1 tile) and below (+3 tiles) from it.
        """

        # TODO there surely is a nicer way to do this...
        # neighbor_offset = {
        #     0: [1, 3],
        #     1: [-1, 1, 3],
        #     2: [-1, 3],
        #     3: [-3, 1, 3],
        #     4: [-3, -1, 1, 3],
        #     5: [-3, -1, 3],
        #     6: [-3, 1],
        #     7: [-3, -1, 1],
        #     8: [-3, -1],
        # }

        neighbor_offset = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        grid_size: int = int(len(self.grid) ** 0.5)
        next_nodes: list[Node] = []
        empty_tile_index = self.grid.index(None)
        row, col = divmod(empty_tile_index, grid_size) #get current row and colum
        for offset_row, offset_col in neighbor_offset:
            new_row = row + offset_row
            new_col = col + offset_col
            if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                new_index = new_row * grid_size + new_col
                temp_node = deepcopy(self)
                temp_node._swap_tiles(empty_tile_index, new_index)
                temp_node.level = self.level + 1
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
        self.expanded_nodes = 0


    def f_val(self, node: Node) -> int:
        """Returns total cost, consisting of actual cost and possible heuristic cost."""
        return node.get_level() + self.heuristic.calc_heuristic_cost(node.grid, node.goal_state)

    def h_val(self, node: Node) -> int:
        """Get cost as calculated by chosen heuristic."""
        return self.heuristic.calc_heuristic_cost(node.grid, node.goal_state)

    def solve(self):
        open_nodes = []
        visited_nodes = set()

        try:
            initial_node = Node(self.initial_grid, self.goal_state)
        except GridException as e:
            print(e)
            return None

        if not initial_node.solvable:
            print("The provided grid is not solvable.")
            return None

        heapq.heappush(open_nodes, (self.f_val(initial_node), initial_node))
        visited_nodes.add(tuple(initial_node.grid))

        expanded_nodes = 0  # Counter for the number of expanded nodes

        while open_nodes:
            current_node = heapq.heappop(open_nodes)[1]

            if current_node._is_goal_state():
                level =  str(current_node.get_level())
                print(f"Goal reached in # moves: {level}")
                print(f"Total nodes expanded: {expanded_nodes}")
                return current_node

            for child in current_node._get_next_nodes():
                if tuple(child.grid) not in visited_nodes:
                    heapq.heappush(open_nodes, (self.f_val(child), child))
                    visited_nodes.add(tuple(child.grid))

            self.expanded_nodes += 1  # Increment the counter each time a node is expanded

        return None


def generate_random_states(num_states):
    random_states = []
    for _ in range(num_states):
        random_states.append(Node.create_random_grid())  # Create a random grid and add it to the list
    return random_states

def analyze_results(manhattan_results, hamming_results):
    manhattan_times = [result[0] for result in manhattan_results]
    manhattan_nodes = [result[1] for result in manhattan_results]

    hamming_times = [result[0] for result in hamming_results]
    hamming_nodes = [result[1] for result in hamming_results]

    # Calculate statistics
    manhattan_time_mean = statistics.mean(manhattan_times)
    manhattan_time_std = statistics.stdev(manhattan_times)

    manhattan_nodes_mean = statistics.mean(manhattan_nodes)
    manhattan_nodes_std = statistics.stdev(manhattan_nodes)

    hamming_time_mean = statistics.mean(hamming_times)
    hamming_time_std = statistics.stdev(hamming_times)

    hamming_nodes_mean = statistics.mean(hamming_nodes)
    hamming_nodes_std = statistics.stdev(hamming_nodes)

    print("Manhattan Heuristic:")
    print(f"Average time: {manhattan_time_mean:.5f} seconds, Standard deviation: {manhattan_time_std:.5f}")
    print(f"Average nodes expanded: {manhattan_nodes_mean:.0f}, Standard deviation: {manhattan_nodes_std:.0f}")

    print("\nHamming Heuristic:")
    print(f"Average time: {hamming_time_mean:.5f} seconds, Standard deviation: {hamming_time_std:.5f}")
    print(f"Average nodes expanded: {hamming_nodes_mean:.0f}, Standard deviation: {hamming_nodes_std:.0f}")


if __name__ == "__main__":
    goal_state = [None, 1, 2, 3, 4, 5, 6, 7, 8]
    # initial_grid = Node.create_random_grid()
    # print(initial_grid)
    #
    # print("Manhattan Heuristic")
    # selected_heuristic = Manhattan()
    # solver = PuzzleSolver(initial_grid, goal_state, selected_heuristic)
    # solution = solver.solve()
    #
    # if solution:
    #     print(f"Solution found! Number of moves needed with Manhattan: {solution.get_level()}\n")
    # else:
    #     print("No solution exists.\n")
    #
    # print("Hamming Heuristic")
    # selected_heuristic = Hamming()
    # solver = PuzzleSolver(initial_grid, goal_state, selected_heuristic)
    # solution_hamming = solver.solve()
    #
    # if solution_hamming:
    #     print(f"Solution found! Number of moves needed with Hamming: {solution_hamming.get_level()}")
    # else:
    #     print("No solution exists.")

    num_states = 100
    random_states = generate_random_states(num_states)

    manhattan_results = []
    hamming_results = []

    # Run the solver for each random state with Manhattan heuristic
    for state in random_states:
        solver = PuzzleSolver(state, goal_state, Manhattan())

        # Track start time
        start_time = time.time()
        solution_manhattan = solver.solve()
        end_time = time.time()

        # Calculate the time taken and number of nodes expanded
        time_taken = end_time - start_time
        nodes_expanded = solver.expanded_nodes

        manhattan_results.append((time_taken, nodes_expanded))

    # Run the solver for each random state with Hamming heuristic
    for state in random_states:
        solver = PuzzleSolver(state, goal_state, Hamming())

        # Track start time
        start_time = time.time()
        solution_hamming = solver.solve()
        end_time = time.time()

        # Calculate the time taken and number of nodes expanded
        time_taken = end_time - start_time
        nodes_expanded = solver.expanded_nodes

        hamming_results.append((time_taken, nodes_expanded))

    analyze_results(manhattan_results, hamming_results)
