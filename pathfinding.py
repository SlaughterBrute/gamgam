import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to this node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost

    def __lt__(self, other):
        return self.f < other.f

def astar(start, goal, grid):
    if type(grid) is list:
        return _astar(start, goal, grid, is_dict=False)
    elif type(grid) is dict:
        return  _astar(start, goal, grid, is_dict=True)

    raise ValueError(f'Supplied grid of type {type(grid)} is not supported.')


def _astar(start, goal, grid, is_dict=False):
    open_list = []
    closed_list = set()

    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        current_node = heapq.heappop(open_list)[1]
        closed_list.add(current_node.position)

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 possible directions
        for new_position in neighbors:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Check if the new position is valid and walkable
            if is_dict:
                if node_position in grid and grid[node_position] == 0:
                    pass
                else:
                    continue
            else:
                if (0 <= node_position[0] < len(grid)) and (0 <= node_position[1] < len(grid[0])) and grid[node_position[0]][node_position[1]] == 0:
                    pass
                else:
                    continue

            if node_position in closed_list:
                continue

            neighbor_node = Node(node_position, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = ((goal_node.position[0] - neighbor_node.position[0]) ** 2) + ((goal_node.position[1] - neighbor_node.position[1]) ** 2)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if not any(neighbor_node.position == item[1].position and neighbor_node.g > item[1].g for item in open_list):
                heapq.heappush(open_list, (neighbor_node.f, neighbor_node))

    return None  # No path found


if __name__ == "__main__":
    grid = [
        [0, 0, 1, 0, 0],  # 0 = walkable, 1 = wall
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]

    print(astar((0,0), (0,1), grid))