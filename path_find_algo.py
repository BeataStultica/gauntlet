import copy
from queue import PriorityQueue


def path_find(maps, mobs=False):
    full_map = copy.deepcopy(maps.tilemap1)
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
        return 0  # ((node[0] - n[0])**2 + (node[1] - n[1])**2)**(1/2)/2
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
