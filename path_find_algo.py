import copy
from queues import PriorityQueue


def path_find(maps, mobs=False):
    full_map = maps.tilemap1
    """
    mobs_center_coord = []
    for i in mobs:
        if i == mob:
            continue
        mobs_center_coord.append(
            [int(i.rect.centerx/40), int(i.rect.centery/40)])
    
    for i in mobs_center_coord:
        full_map[i[1]][i[0]] = 1
    """
    graph_to_key = {}
    graph_to_exit = {}
    forb_to_key = [1, 7, 9]
    forb_to_exit = [1]
    for i in range(len(full_map)):
        for j in range(len(full_map[i])):
            if full_map[i][j] not in forb_to_key:
                if full_map[i+1][j] not in forb_to_key and graph_to_key.get((i, j)) is None:
                    graph_to_key[(i, j)] = [(i+1, j)]
                elif full_map[i+1][j] not in forb_to_key:
                    graph_to_key[(i, j)].append((i+1, j))
                if full_map[i-1][j] not in forb_to_key and graph_to_key.get((i, j)) is None:
                    graph_to_key[(i, j)] = [(i-1, j)]
                elif full_map[i-1][j] not in forb_to_key:
                    graph_to_key[(i, j)].append((i-1, j))
                if full_map[i][j-1] not in forb_to_key and graph_to_key.get((i, j)) is None:
                    graph_to_key[(i, j)] = [(i, j-1)]
                elif full_map[i][j-1] not in forb_to_key:
                    graph_to_key[(i, j)].append((i, j-1))
                if full_map[i][j+1] not in forb_to_key and graph_to_key.get((i, j)) is None:
                    graph_to_key[(i, j)] = [(i, j+1)]
                elif full_map[i][j+1] not in forb_to_key:
                    graph_to_key[(i, j)].append((i, j+1))
            if full_map[i][j] not in forb_to_exit:
                if full_map[i+1][j] not in forb_to_exit and graph_to_exit.get((i, j)) is None:
                    graph_to_exit[(i, j)] = [(i+1, j)]
                elif full_map[i+1][j] not in forb_to_exit:
                    graph_to_exit[(i, j)].append((i+1, j))
                if full_map[i-1][j] not in forb_to_exit and graph_to_exit.get((i, j)) is None:
                    graph_to_exit[(i, j)] = [(i-1, j)]
                elif full_map[i-1][j] not in forb_to_exit:
                    graph_to_exit[(i, j)].append((i-1, j))
                if full_map[i][j-1] not in forb_to_exit and graph_to_exit.get((i, j)) is None:
                    graph_to_exit[(i, j)] = [(i, j-1)]
                elif full_map[i][j-1] not in forb_to_exit:
                    graph_to_exit[(i, j)].append((i, j-1))
                if full_map[i][j+1] not in forb_to_exit and graph_to_exit.get((i, j)) is None:
                    graph_to_exit[(i, j)] = [(i, j+1)]
                elif full_map[i][j+1] not in forb_to_exit:
                    graph_to_exit[(i, j)].append((i, j+1))
    key_coor = None
    exit_coor = None
    for i in range(len(full_map)):
        if 8 in full_map[i]:
            key_coor = (i, full_map[i].index(8))
        if 9 in full_map[i]:
            exit_coor = (i, full_map[i].index(9))
    return (graph_to_key, graph_to_exit, key_coor, exit_coor)


def path_find_mobs(curr_graph, mobs, mob=None):
    for i in mobs:
        if i == mob:
            continue
        x = int(i.rect.centerx/40)
        y = int(i.rect.centery/40)
        curr_graph.pop((y, x), None)
        if (y-1, x) in curr_graph:
            if (y, x) in curr_graph[(y-1, x)]:
                curr_graph[(y-1, x)].remove((y, x))
        if (y+1, x) in curr_graph:
            if (y, x) in curr_graph[(y+1, x)]:
                curr_graph[(y+1, x)].remove((y, x))
        if (y, x+1) in curr_graph:
            if (y, x) in curr_graph[(y, x+1)]:
                curr_graph[(y, x+1)].remove((y, x))
        if (y, x-1) in curr_graph:
            if (y, x) in curr_graph[(y, x-1)]:
                curr_graph[(y, x-1)].remove((y, x))
    return curr_graph


def generate_map_dict(maps, ai_settings, tilemap=False):
    if tilemap:
        full_map = tilemap
    else:
        full_map = copy.deepcopy(maps.tilemap1)
    graph = {}

    for i in range(len(full_map)-1):
        for j in range(len(full_map[i])-1):
            if full_map[i][j] == 0:
                if full_map[i+1][j] == 0 and graph.get((i, j)) is None:
                    graph[(i, j)] = [(i+1, j)]
                elif full_map[i+1][j] == 0:
                    graph[(i, j)].append((i+1, j))
                if full_map[i-1][j] == 0 and graph.get((i, j)) is None:
                    graph[(i, j)] = [(i-1, j)]
                elif full_map[i-1][j] == 0:
                    graph[(i, j)].append((i-1, j))
                if full_map[i][j-1] == 0 and graph.get((i, j)) is None:
                    graph[(i, j)] = [(i, j-1)]
                elif full_map[i][j-1] == 0:
                    graph[(i, j)].append((i, j-1))
                if full_map[i][j+1] == 0 and graph.get((i, j)) is None:
                    graph[(i, j)] = [(i, j+1)]
                elif full_map[i][j+1] == 0:
                    graph[(i, j)].append((i, j+1))
    if tilemap:
        return graph
    else:
        ai_settings.maps_dict = graph


def dfs(graph_adj, start, end):
    stack = [(start, [start])]
    visited = []
    while stack:
        (v, path) = stack.pop()

        if v not in visited:
            if v == end:
                return path
            visited.append(v)
            for n in graph_adj[v]:
                if n not in visited:
                    stack.append((n, path + [n]))
    return []


def bfs(graph, start, end):
    visited = []
    queue = [[start]]
    if start == end:
        return []
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited and node in graph:
            neighbours = graph[node]
            for n in neighbours:
                if n not in visited:
                    new_path = list(path)
                    new_path.append(n)
                    queue.append(new_path)
                    if n == end:
                        return new_path
            visited.append(node)
    return []


def ucs(graph, start, end):
    visited = []
    queue = PriorityQueue()
    queue.put((0, start, [start]))
    if start == end:
        return []
    while queue:
        cost, node, path = queue.get()
        if node not in visited:
            neighbours = graph[node]
            for n in neighbours:
                if n not in visited:
                    queue.put((cost+1, n, path+[n]))
                    if n == end:
                        return path + [n]
            visited.append(node)
    return []


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    if current is None:
        return []
    while current != start:
        if current not in came_from:
            break
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def heuristic(node, n):
    if node and n:
        return ((node[0] - n[0])**2 + (node[1] - n[1])**2)**(1/2)
    else:
        return 0


def a_star_search(graph, start, end):
    queue = PriorityQueue()
    queue.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not queue.empty():
        node = queue.get()

        if node == end:
            break
        if node in graph:
            neighbours = graph[node]
            for next in neighbours:
                new_cost = cost_so_far[node] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(end, next)
                    queue.put(next, priority)
                    came_from[next] = node

    return reconstruct_path(came_from, start, end)


a = {(1, 1): [(2, 1), (1, 2)], (1, 2): [(1, 1), (1, 3)], (1, 3): [(1, 2)], (1, 7): [(2, 7), (1, 8)], (1, 8): [(2, 8), (1, 7), (1, 9)], (1, 9): [(2, 9), (1, 8), (1, 10)], (1, 10): [(1, 9), (1, 11)], (1, 11): [(2, 11), (1, 10), (1, 12)], (1, 12): [(2, 12), (1, 11)], (1, 14): [(2, 14), (1, 15)], (1, 15): [(2, 15), (1, 14), (1, 16)], (1, 16): [(2, 16), (1, 15), (1, 17)], (1, 17):
     [(2, 17), (1, 16), (1, 18)], (1, 18): [(2, 18), (1, 17), (1, 19)], (1, 19): [(2, 19), (1, 18), (1, 20)], (1, 20): [(1, 19), (1, 21)], (1, 21): [(2, 21), (1, 20)], (2, 1): [(1, 1)], (2, 7): [(3, 7), (1, 7), (2, 8)], (2, 8): [(3, 8), (1, 8), (2, 7), (2, 9)], (2, 9): [(3, 9), (1, 9), (2, 8)], (2, 11): [(3, 11), (1, 11), (2, 12)], (2, 12): [(1, 12), (2, 11), (2, 13)], (2, 13): [(2, 12), (2, 14)], (2, 14): [(3, 14), (1, 14), (2, 13), (2, 15)], (2, 15): [(3, 15), (1, 15), (2, 14), (2, 16)], (2, 16): [(1, 16), (2, 15), (2, 17)], (2, 17): [(1, 17), (2, 16), (2, 18)], (2, 18): [(1, 18), (2, 17), (2, 19)], (2, 19): [(3, 19), (1, 19), (2, 18)], (2, 21): [(3, 21), (1, 21)], (3, 4): [(4, 4), (3, 5)], (3, 5): [(4, 5), (3, 4)], (3, 7): [(4, 7), (2, 7), (3, 8)], (3, 8): [(4, 8), (2, 8), (3, 7), (3, 9)], (3, 9): [(4, 9), (2, 9), (3, 8)], (3, 11): [(4, 11), (2, 11)], (3, 14): [(4, 14), (2, 14), (3, 15)], (3, 15): [(4, 15), (2, 15), (3, 14)], (3, 19): [(4, 19), (2, 19)], (3, 21): [(4, 21), (2, 21)], (4,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          1): [(5, 1)], (4, 3): [(5, 3), (4, 4)], (4, 4): [(5, 4), (3, 4), (4, 3), (4, 5)], (4, 5): [(5, 5), (3, 5), (4, 4), (4, 6)], (4, 6): [(5, 6), (4, 5), (4, 7)], (4, 7): [(5, 7), (3, 7), (4, 6), (4, 8)], (4, 8): [(5, 8), (3, 8), (4, 7), (4, 9)], (4, 9):
     [(5, 9), (3, 9), (4, 8), (4, 10)], (4, 10): [(4, 9), (4, 11)], (4, 11): [(3, 11), (4, 10), (4, 12)], (4, 12): [(4, 11), (4, 13)], (4, 13): [(4, 12), (4, 14)], (4, 14): [(5, 14), (3, 14), (4, 13), (4, 15)], (4, 15): [(5, 15), (3, 15), (4, 14), (4, 16)], (4, 16): [(4, 15), (4, 17)], (4, 17): [(4, 16), (4, 18)], (4, 18): [(4, 17), (4, 19)], (4, 19): [(5, 19), (3, 19), (4, 18)], (4, 21): [(5, 21), (3, 21)], (5, 1): [(6, 1), (4, 1)], (5, 3): [(6, 3), (4, 3), (5, 4)], (5, 4): [(4, 4), (5, 3), (5, 5)], (5, 5): [(6, 5), (4, 5), (5, 4), (5, 6)], (5, 6): [(6, 6), (4, 6), (5, 5), (5, 7)], (5, 7): [(4, 7), (5, 6), (5, 8)], (5, 8): [(6, 8), (4, 8), (5, 7), (5, 9)], (5, 9): [(6, 9), (4, 9), (5, 8)], (5, 14): [(6, 14), (4, 14), (5, 15)], (5, 15): [(6, 15), (4, 15), (5, 14)], (5, 19): [(4, 19), (5, 20)], (5, 20): [(5, 19), (5, 21)], (5, 21): [(6, 21), (4, 21), (5, 20)], (6, 1):
     [(7, 1), (5, 1), (6, 2)], (6, 2): [(6, 1), (6, 3)], (6, 3): [(7, 3), (5, 3), (6, 2)], (6, 5): [(7, 5), (5, 5), (6, 6)], (6, 6): [(7, 6), (5, 6), (6, 5)], (6, 8): [(7, 8), (5, 8), (6, 9)], (6, 9): [(7, 9), (5, 9), (6, 8)], (6, 14): [(7, 14), (5, 14),
                                                                                                                                                                                                                                             (6, 15)], (6, 15): [(7, 15), (5, 15), (6, 14)], (6, 21): [(7, 21), (5, 21)], (7, 1): [(6, 1)], (7, 3): [(8, 3), (6, 3), (7, 4)], (7, 4): [(8, 4), (7, 3), (7, 5)], (7, 5): [(8, 5), (6, 5), (7, 4), (7, 6)], (7, 6): [(8, 6), (6, 6), (7, 5)], (7, 8): [(8, 8), (6, 8), (7, 9)], (7, 9): [(8, 9), (6, 9), (7, 8)], (7, 14): [(8, 14), (6, 14), (7, 15)], (7, 15): [(8, 15), (6, 15), (7, 14)], (7, 17): [(8, 17)], (7, 21): [(8, 21), (6, 21)], (8, 2): [(9, 2), (8, 3)], (8, 3): [(7, 3), (8, 2), (8, 4)], (8, 4):
     [(9, 4), (7, 4), (8, 3), (8, 5)], (8, 5): [(9, 5), (7, 5), (8, 4), (8, 6)], (8, 6): [(9, 6), (7, 6), (8, 5)], (8, 8): [(9, 8), (7, 8), (8, 9)], (8, 9): [(9, 9), (7, 9), (8, 8)], (8, 14): [(7, 14), (8, 15)], (8, 15): [(9, 15), (7, 15), (8, 14)], (8, 17): [(9, 17), (7, 17)], (8, 21): [(9, 21), (7, 21)], (9, 2): [(10, 2), (8, 2)], (9, 4): [(10, 4), (8, 4), (9, 5)], (9, 5): [(8, 5), (9, 4), (9, 6)], (9, 6): [(10, 6), (8, 6), (9, 5)], (9, 8): [(8, 8), (9, 9)], (9, 9): [(10, 9), (8, 9), (9, 8), (9, 10)], (9, 10): [(9, 9), (9, 11)], (9, 11): [(9, 10), (9, 12)], (9, 12): [(9, 11), (9, 13)], (9, 13): [(9, 12)], (9, 15): [(10,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 15), (8, 15)], (9, 17): [(10, 17), (8, 17)], (9, 21): [(10, 21), (8, 21)], (10, 2): [(11, 2), (9, 2), (10, 3)], (10, 3): [(11, 3), (10, 2), (10, 4)], (10, 4): [(11, 4), (9, 4), (10, 3)], (10, 6): [(11, 6), (9, 6)], (10, 9): [(9, 9)], (10, 14): [(11,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       14), (10, 15)], (10, 15): [(11, 15), (9, 15), (10, 14)], (10, 17): [(11, 17), (9, 17)], (10, 21): [(11, 21), (9, 21)], (11, 2): [(12, 2), (10, 2), (11, 3)], (11, 3): [(10, 3), (11, 2), (11, 4)], (11, 4): [(12, 4), (10, 4), (11, 3), (11, 5)], (11, 5): [(12, 5), (11, 4), (11, 6)], (11, 6): [(12, 6), (10, 6), (11, 5)], (11, 14): [(12, 14), (10, 14), (11, 15)], (11, 15): [(10, 15), (11, 14), (11, 16)], (11, 16): [(11, 15), (11, 17)], (11, 17): [(12, 17), (10, 17), (11, 16)], (11, 21): [(12, 21), (10, 21)], (12, 2): [(13, 2), (11, 2)], (12, 4): [(13, 4), (11, 4), (12, 5)], (12, 5): [(13, 5), (11, 5), (12, 4), (12, 6)], (12, 6): [(13, 6), (11, 6), (12, 5)], (12, 14): [(13, 14), (11, 14)], (12, 17): [(13, 17), (11, 17)], (12, 21): [(13, 21), (11,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 21)], (13, 1): [(13, 2)], (13, 2): [(12, 2), (13, 1), (13, 3)], (13, 3): [(13, 2), (13, 4)], (13, 4): [(12, 4), (13, 3), (13, 5)], (13, 5): [(12, 5), (13, 4), (13, 6)], (13, 6): [(12, 6), (13, 5), (13, 7)], (13, 7): [(13, 6), (13, 8)], (13, 8): [(13, 7), (13, 9)], (13, 9): [(13, 8), (13, 10)], (13, 10): [(13, 9)], (13, 14): [(12, 14), (13, 15)], (13, 15): [(13, 14), (13, 16)], (13, 16): [(13, 15), (13, 17)], (13, 17): [(12, 17), (13, 16), (13, 18)], (13, 18): [(13, 17), (13, 19)], (13, 19): [(13, 18), (13, 20)], (13, 20): [(13, 19), (13, 21)], (13, 21): [(12, 21), (13, 20)]}

#print(bfs(a, (12, 3), (9, 14)))
