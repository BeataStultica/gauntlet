from path_find_algo import bfs, path_find
import pygame
import random
import pickle
import copy


class Map:
    def __init__(self):
        #self.tilemap1 = [[1 for i in range(0, 23)] for j in range(0, 15)]
        with open('map.data', 'rb') as f:
            a = pickle.load(f)
         #   print(a)
        self.tilemap1 = copy.deepcopy(a)
        self.x = 3
        self.y = 12
        self.key_amount = 1
        self.levels = {1: self.tilemap1,
                       2: self.tilemap1, 3: self.tilemap1, 4: self.tilemap1, 5: self.tilemap1, 6: self.tilemap1, 7: 'win'}
        self.textures_floor = pygame.image.load('assets/floot.png').convert()
        self.textures_floor = pygame.transform.scale(
            self.textures_floor, (282, 146))
        self.textures_walls = pygame.image.load('assets/walls2.png').convert()
        self.textures_exit = pygame.image.load('assets/exit.png').convert()
        self.textures_exit = pygame.transform.scale(
            self.textures_exit, (40, 40))

    def lvl_generate(self):

        with open('map.data', 'rb') as f:
            a = pickle.load(f)
        #    print(a)
        self.tilemap1 = copy.deepcopy(a)
    '''
        x = random.randint(1, 21)
        y = random.randint(1, 13)
        self.x = x
        self.y = y
        self.key_amount = 1
        treas_amount = 11  # random.randint(2, 6)
        food_amount = 0  # random.randint(2, 6)
        spawn_mob = random.randint(1, 2)
        exit_x = 0
        exit_y = 0
        key_x = 0
        key_y = 0
        tonnels_numb = 80
        max_len = 9
        while tonnels_numb != 0:
            if ((self.x - x)**2 + (self.y-y)**2)**(1/2) > 10 and exit_x == 0:
                self.tilemap1[y][x] = 9
                exit_x = x
                exit_y = y
            if exit_x != 0 and ((exit_x - x)**2 + (exit_y-y)**2)**(1/2) > 10 and ((self.x - x)**2 + (self.y-y)**2)**(1/2) > 6 and key_x == 0:
                self.tilemap1[y][x] = 8
                key_x = x
                key_y = y
            curr_len = random.randint(1, max_len)
            curr_x = x
            curr_y = y
            side = random.randint(1, 4)
            if side == 1:
                while curr_len != 0:
                    if x != 0 and self.tilemap1[y][x] == 1:
                        self.tilemap1[y][x] = 0
                    if x != 1:
                        x -= 1
                    else:
                        break
                    curr_len -= 1
            elif side == 2:
                while curr_len != 0:
                    if x != 22 and self.tilemap1[y][x] == 1:
                        self.tilemap1[y][x] = 0
                    if x != 21:
                        x += 1
                    else:
                        break
                    curr_len -= 1
            elif side == 3:
                while curr_len != 0:
                    if y != 0 and self.tilemap1[y][x] == 1:
                        self.tilemap1[y][x] = 0
                    if y != 1:
                        y -= 1
                    else:
                        break
                    curr_len -= 1
            elif side == 4:
                while curr_len != 0:
                    if y != 14 and self.tilemap1[y][x] == 1:
                        self.tilemap1[y][x] = 0
                    if y != 13:
                        y += 1
                    else:
                        break
                    curr_len -= 1
            if curr_x != x or curr_y != y:
                tonnels_numb -= 1
        if key_x == 0:
            while True:
                x = random.randint(1, 21)
                y = random.randint(1, 13)
                distan = ((self.x-x)**2+(self.y-y)**2)**(1/2)
                if self.tilemap1[y][x] == 0 and distan > 2:
                    self.tilemap1[y][x] == 8
                    break
        if exit_x == 0:
            while True:
                x = random.randint(1, 21)
                y = random.randint(1, 13)
                distan = ((self.x-x)**2+(self.y-y)**2)**(1/2)
                if self.tilemap1[y][x] == 0 and distan > 2:
                    self.tilemap1[y][x] == 9
                    break
        near_exit = [[exit_y-1, exit_x], [exit_y, exit_x-1], [exit_y+1, exit_x], [exit_y, exit_x+1],
                     [exit_y-1, exit_x-1], [exit_y+1, exit_x+1], [exit_y+1, exit_x-1], [exit_y-1, exit_x+1]]
        for i in near_exit:
            if self.tilemap1[i[0]][i[1]] != 1 and self.tilemap1[i[0]][i[1]] != 8:
                self.tilemap1[i[0]][i[1]] = 7
        while treas_amount:
            x = random.randint(1, 21)
            y = random.randint(1, 13)
            if self.tilemap1[y][x] == 0:
                self.tilemap1[y][x] = 4
                treas_amount -= 1
        while food_amount:
            x = random.randint(1, 21)
            y = random.randint(1, 13)
            if self.tilemap1[y][x] == 0:
                self.tilemap1[y][x] = 5
                food_amount -= 1
        while spawn_mob:
            x = random.randint(1, 21)
            y = random.randint(1, 13)
            if self.tilemap1[y][x] == 0 and self.tilemap1[y][x-1] == 0 and (x, y) != (self.x, self.y):
                self.tilemap1[y][x] = 3
                spawn_mob -= 1
        if self.y-1 != 0:
            self.tilemap1[self.y-1][self.x] = 0
        if self.y+1 != 14:
            self.tilemap1[self.y+1][self.x] = 0
        if self.x-1 != 0:
            self.tilemap1[self.y][self.x-1] = 0
        if self.x+1 != 22:
            self.tilemap1[self.y][self.x+1] = 0
        (graph_to_key, graph_to_exit, key_coor, exit_coor) = path_find(
            self)

        if len(bfs(graph_to_key, (self.y, self.x), key_coor)) == 0:
            self.lvl_generate()

        with open('map.data', 'wb') as f:
            pickle.dump(self.tilemap1, f)
        '''
