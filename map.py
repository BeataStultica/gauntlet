from key_actions import spawn_mob
import pygame
import random


class Map:
    def __init__(self):
        self.tilemap1 = [[1 for i in range(0, 23)] for j in range(0, 15)]
        self.x = 1
        self.y = 1

        self.levels = {1: self.tilemap1,
                       2: self.tilemap1, 3: self.tilemap1, 4: 'win'}
        self.textures_floor = pygame.image.load('assets/floot.png').convert()
        self.textures_floor = pygame.transform.scale(
            self.textures_floor, (282, 146))
        self.textures_walls = pygame.image.load('assets/walls2.png').convert()
        self.textures_exit = pygame.image.load('assets/exit.png').convert()
        self.textures_exit = pygame.transform.scale(
            self.textures_exit, (40, 40))

    def lvl_generate(self):
        x = random.randint(1, 21)
        y = random.randint(1, 13)
        self.x = x
        self.y = y
        treas_amount = random.randint(2, 6)
        food_amount = random.randint(2, 6)
        spawn_mob = random.randint(1, 3)
        exit_x = 0
        exit_y = 0
        key_x = 0
        key_y = 0
        tonnels_numb = 90
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
                if self.tilemap1[y][x] == 0:
                    self.tilemap1[y][x] == 8
                    break
        if exit_x == 0:
            while True:
                x = random.randint(1, 21)
                y = random.randint(1, 13)
                if self.tilemap1[y][x] == 0:
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
            if self.tilemap1[y][x] == 0 and self.tilemap1[y][x-1] == 0:
                self.tilemap1[y][x] = 3
                spawn_mob -= 1
