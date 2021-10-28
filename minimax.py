from treeBuild import Leaf
import copy
from treeBuild import game_copy


class Minimax:
    def __init__(self, util_func, result_func, settings, max_depth=4):
        self.util_func = util_func
        self.result_func = result_func
        self.max_depth = max_depth
        self.settings = settings

    def alpha_beta_search(self, tree):

        v, i = self.max_value(tree.root, float('-inf'), float('inf'), 0)
        return v, i

    def max_value(self, node, a, b, depth):
        if isinstance(node, Leaf) or depth >= self.max_depth:
            # print(node.calculate_utility(self.util_func))
            return node.calculate_utility(self.util_func, self.settings), 0

        # data = node.get_data()
        v = float('-inf')
        best_i = -1

        for i in node.get_children().keys():
            # data_copy = game_copy(data)

            result_node = self.result_func(node, i)
            if result_node.get_data().get_player_turn() == 1:
                v = max(v, self.max_value(result_node, a, b, depth + 1)[0])
            else:
                v = max(v, self.min_value(result_node, a, b, depth + 1)[0])

            # альфа-бета
            if v >= b:
                return v, best_i

            if v > a:
                best_i = i

            a = max(a, v)

        return v, best_i

    def min_value(self, node, a, b, depth):
        if isinstance(node, Leaf) or depth >= self.max_depth:
            # print(node.calculate_utility(self.util_func))
            return node.calculate_utility(self.util_func, self.settings), 0

        # data = node.get_data()
        v = float('inf')
        best_i = -1

        for i in node.get_children().keys():
            # data_copy = game_copy(data)

            result_node = self.result_func(node, i)
            if result_node.get_data().get_player_turn() == 1:
                v = min(v, self.max_value(result_node, a, b, depth + 1)[0])
            else:
                v = min(v, self.min_value(result_node, a, b, depth + 1)[0])
            # альфа-бета
            if v <= a:
                return v, best_i

            if v < b:
                best_i = i

            b = min(b, v)
        return v, best_i

    def expectimax(self, tree):
        v, i = self.max_value_exp(tree.root, 0)
        return v, i

    def max_value_exp(self, node, depth):
        if isinstance(node, Leaf) or depth >= self.max_depth:
            # print(node.calculate_utility(self.util_func))
            return node.calculate_utility(self.util_func, self.settings), 0

        # data = node.get_data()
        v = float('-inf')
        best_i = -1

        for i in node.get_children().keys():
            # data_copy = game_copy(data)

            result_node = self.result_func(node, i)
            if result_node.get_data().get_player_turn() == 1:
                v = max(v, self.max_value_exp(result_node,  depth + 1)[0])
            else:
                v = max(v, self.min_value_exp(result_node,  depth + 1)[0])

        return v, best_i

    def min_value_exp(self, node, depth):
        if isinstance(node, Leaf) or depth >= self.max_depth:
            # print(node.calculate_utility(self.util_func))
            return node.calculate_utility(self.util_func, self.settings), 0

        # data = node.get_data()
        v = float('inf')
        best_i = -1
        values = 0
        for i in node.get_children().keys():
            # data_copy = game_copy(data)
            result_node = self.result_func(node, i)
            if result_node.get_data().get_player_turn() == 1:
                values += self.max_value_exp(result_node,
                                             depth + 1)[0]
            else:
                values += self.min_value_exp(result_node,
                                             depth + 1)[0]
        if len(node.children) > 0:
            v = values/len(node.children)
        return v, best_i
