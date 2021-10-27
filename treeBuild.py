import copy

from pygame.display import update

from Game import Game


class TreeBuilder:
    def __init__(self, maps, rec_limit=4):
        self.rec_limit = rec_limit
        self.root = None
        self.maps = maps.tilemap1

    def set_root(self, root):
        self.root = root

    def build(self):
        self.build_from(self.root)

    def build_from(self, node, rec_depth=0):
        if rec_depth >= self.rec_limit:
            return
        maps1 = game_copy(node.get_data())
        # print(maps1.mobs)
        maps1.update_map()
        # print(maps1.state)
        enemies_coords = get_enemies_positions(maps1.state)

        # print(enemies_coords)
        if rec_depth % 2 == 0:
            for i in range(1, 5):  # left right, top, bottom
                game = game_copy(node.get_data())
                game.update_map()
                game.player_turn = 0
                if game.move(i):
                    if game.is_terminal_state():
                        game.end_game()
                        node.add_child(move=i, child=Leaf(game))
                    else:
                        node.add_child(move=i, child=Node(game))
        else:
            game = node.get_data()
            neighboring_nodes = [get_neighbors(
                game.state, coord) for coord in enemies_coords]
            variations = get_variations(neighboring_nodes)
            move_num = 1
            for i in variations:
                if len(i) == 0:
                    for i in range(1, 5):  # left right, top, bottom
                        game = game_copy(node.get_data())
                        game.update_map()
                        game.player_turn = 0
                        if game.move(i):
                            if game.is_terminal_state():
                                game.end_game()
                                node.add_child(move=i, child=Leaf(game))
                            else:
                                node.add_child(move=i, child=Node(game))
                else:
                    game = game_copy(node.get_data())
                    game.update_map()
                    game.player_turn = 1
                    game.mobs_coord = i
                    for k in range(len(game.state)):
                        for n in range(len(game.state[0])):
                            if game.state[k][n] == 13:
                                game.state[k][n] = 0
                    for j in i:
                        game.state[j[0]][j[1]] = 13
                    node.add_child(move=move_num, child=Node(game))
                move_num += 1
        for child in node.get_children().values():
            if isinstance(child, Node):
                self.build_from(child, rec_depth + 1)


class Node:
    def __init__(self, data):
        self.data = data
        self.children = {}

    def add_child(self, move, child):
        self.children[move] = child

    def get_children(self):
        return self.children

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def calculate_utility(self, fn):
        return fn(self.data)


class Leaf:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def calculate_utility(self, fn):
        return fn(self.data)


def get_variations(arr):
    result = []

    def get_variations_recurs(last_arr, res):
        if len(last_arr) == 0:
            result.append(res)
            return
        curr_arr = last_arr[0]
        for item in curr_arr:
            get_variations_recurs(last_arr[1:], res + [item])
    get_variations_recurs(arr, [])
    return result


def get_enemies_positions(maps):
    coords = []
    for i in range(len(maps)):
        for j in range(len(maps[0])):
            if maps[i][j] == 13:
                coords.append((i, j))
    return coords


def get_neighbors(matrix, current_coord):
    (cy, cx) = current_coord
    neighboring_nodes = [(cy-1, cx), (cy, cx+1), (cy+1, cx), (cy, cx-1)]

    neighboring_nodes = list(filter(
        lambda node: matrix[node[0]][node[1]] == 0, neighboring_nodes))

    return neighboring_nodes


def game_copy(game):
    new_game = Game(game.map, game.mobs, game.player)
    new_game.state = copy.deepcopy(game.state)
    new_game.player_turn = game.player_turn
    new_game.player_x = game.player_x
    new_game.player_y = game.player_y
    new_game.terminal = game.terminal
    new_game.mobs_coord = copy.deepcopy(game.mobs_coord)
    new_game.update_map()
    return new_game


def update_map(game):
    state = copy.deepcopy(game.map.tilemap1)
    for i in game.mobs:
        print
        x = int(i.rect.centerx/40)
        y = int(i.rect.centery/40)
        state[y][x] == 13
    x = int(game.player.rect.centerx/40)
    y = int(game.player.rect.centery/40)
    game.player_x = x
    game.player_y = y
    if state[y][x] == 9:
        game.terminal == True
    state[y][x] == 14

    return state
