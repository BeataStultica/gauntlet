import copy
import pygame
import random
from path_find_algo import path_find, a_star_search, bfs, generate_map_dict, path_find_mobs


class Enemy(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, x, y, maps, mobs, player, arrows):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.mobs = mobs
        self.arrows = arrows
        self.ai_settings = ai_settings
        self.maps = maps
        self.player = player
        self.path = []
        self.level = maps.levels[self.ai_settings.current_lvl]
        self.block_size = ai_settings.block_size
        self.sheet = pygame.image.load('assets/ghost.png').convert()
        self.sheet = pygame.transform.scale(
            self.sheet, (12*self.block_size, 8*self.block_size))
        self.rect = pygame.Rect((0, 0, self.block_size, self.block_size))
        self.image = pygame.Surface(
            (self.block_size, self.block_size)).convert()
        self.image.blit(self.sheet, (0, 0), self.rect)
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.screen_rect = screen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        self.side = 2  # 1 - r, 2 - l, 3 -b, 4 -t
        self.hp = 10
        self.atk = 200
        self.speed = 2
        self.cost = 10

    def update(self):
        if self.ai_settings.maps_dict is None:
            generate_map_dict(self.maps, self.ai_settings)
        # graph = path_find_mobs(
        #    copy.deepcopy(self.ai_settings.maps_dict), self.mobs, self)
        graph = self.ai_settings.maps_dict
        posy = int(self.rect.centery/self.block_size)
        posx = int(self.rect.centerx/self.block_size)
        playerx = int(self.player.rect.centerx/self.block_size)
        playery = int(self.player.rect.centery/self.block_size)
        for i in self.arrows:
            arrows_path = bfs(graph,
                              (posy, posx), (int(i.rect.centery/40), int(i.rect.centerx/40)))
            graph = copy.deepcopy(self.ai_settings.maps_dict)
            if (int(i.rect.centery/40), int(i.rect.centerx/40)) != (playery, playerx):
                self.evade_arrow(graph, int(
                    i.rect.centery/40), int(i.rect.centerx/40))
            if i.side == 'right':
                # if (int(i.rect.centery/40), int(i.rect.centerx/40)-1) != (playery, playerx) and (int(i.rect.centery/40), int(i.rect.centerx/40)-1) != (playery, playerx+1):
                #    self.evade_arrow(graph, int(
                #        i.rect.centery/40), int(i.rect.centerx/40)-1)
                for j in range(1, int(len(arrows_path)*0.6)+1):
                    self.evade_arrow(graph, int(
                        i.rect.centery/40), int(i.rect.centerx/40)+j)
            elif i.side == 'left':
                # if (int(i.rect.centery/40), int(i.rect.centerx/40)+1) != (playery, playerx) and (int(i.rect.centery/40), int(i.rect.centerx/40)+1) != (playery, playerx-1):
                #    self.evade_arrow(graph, int(
                #        i.rect.centery/40), int(i.rect.centerx/40)+1)
                for j in range(1, int(len(arrows_path)*0.6)+1):
                    self.evade_arrow(graph, int(
                        i.rect.centery/40), int(i.rect.centerx/40)-j)
            elif i.side == 'up':
                # if (int(i.rect.centery/40)+1, int(i.rect.centerx/40)) != (playery, playerx) and (int(i.rect.centery/40)+1, int(i.rect.centerx/40)) != (playery-1, playerx):
                #    self.evade_arrow(graph, int(
                #        i.rect.centery/40)+1, int(i.rect.centerx/40))
                for j in range(1, int(len(arrows_path)*0.6)+1):
                    self.evade_arrow(graph, int(
                        i.rect.centery/40)-j, int(i.rect.centerx/40))
            elif i.side == 'down':
                # if (int(i.rect.centery/40)-1, int(i.rect.centerx/40)) != (playery, playerx) and (int(i.rect.centery/40)-1, int(i.rect.centerx/40))!= (playery+1, playerx):
                #    self.evade_arrow(graph, int(
                #        i.rect.centery/40)-1, int(i.rect.centerx/40))
                for j in range(1, int(len(arrows_path)*0.6)+1):
                    self.evade_arrow(graph, int(
                        i.rect.centery/40)+j, int(i.rect.centerx/40))
        self.path = bfs(
            graph, (posy, posx), (playery, playerx))
        mobs_l = []
        mobs_r = []
        mobs_t = []
        mobs_b = []

        if len(self.path) > 1 and abs(self.rect.x - self.path[1][1]*40) < 2:
            if int(self.rect.y/40) - self.path[1][0] == 1:
                self.side = 4
            if int(self.rect.centery/40) - self.path[1][0] == -1:
                self.side = 3
        elif len(self.path) > 1 and abs(self.rect.y - self.path[1][0]*40) < 2:
            if int(self.rect.centerx/40) - self.path[1][1] == 1:
                self.side = 2
            if int(self.rect.centerx/40) - self.path[1][1] == -1:
                self.side = 1
        for i in self.mobs:
            if i == self:
                continue
            if self.side == 1:
                if i.side == 1 and ((i.x - self.x)**2 + (i.y - self.y)**2)**(1/2) < 28:
                    mobs_r.append(i)
                elif i.side == 2 and (((i.x-i.speed) - (self.x+self.speed))**2 + (i.y - self.y)**2)**(1/2) < 28:
                    mobs_r.append(i)
                elif i.side == 3 and ((i.x - (self.x+self.speed))**2 + ((i.y+i.speed) - self.y)**2)**(1/2) < 28:
                    mobs_r.append(i)
                elif i.side == 4 and ((i.x - (self.x+self.speed))**2 + ((i.y-i.speed) - self.y)**2)**(1/2) < 30:
                    mobs_r.append(i)
            elif self.side == 2:
                if i.side == 1 and (((i.x+i.speed) - (self.x-self.speed))**2 + (i.y - self.y)**2)**(1/2) < 28:
                    mobs_l.append(i)
                elif i.side == 2 and ((i.x - self.x)**2 + (i.y - self.y)**2)**(1/2) < 28:
                    mobs_l.append(i)
                elif i.side == 3 and ((i.x - (self.x-self.speed))**2 + ((i.y+i.speed) - self.y)**2)**(1/2) < 28:
                    mobs_l.append(i)
                elif i.side == 4 and ((i.x - (self.x-self.speed))**2 + ((i.y-i.speed) - self.y)**2)**(1/2) < 30:
                    mobs_l.append(i)
            elif self.side == 3:
                if i.side == 1 and (((i.x + i.speed) - self.x)**2 + (i.y - (self.y+self.speed))**2)**(1/2) < 28:
                    mobs_b.append(i)
                elif i.side == 2 and (((i.x - i.speed) - self.x)**2 + (i.y - (self.y+self.speed))**2)**(1/2) < 28:
                    mobs_b.append(i)
                elif i.side == 3 and ((i.x - self.x)**2 + (i.y - self.y)**2)**(1/2) < 30:
                    mobs_b.append(i)
                elif i.side == 4 and ((i.x - self.x)**2 + ((i.y-i.speed) - (self.y+self.speed))**2)**(1/2) < 30:
                    mobs_b.append(i)
            else:
                if i.side == 1 and (((i.x + i.speed) - self.x)**2 + (i.y - (self.y-self.speed))**2)**(1/2) < 28:
                    mobs_t.append(i)
                elif i.side == 2 and (((i.x - i.speed) - self.x)**2 + (i.y - (self.y-self.speed))**2)**(1/2) < 28:
                    mobs_t.append(i)
                elif i.side == 3 and ((i.x - self.x)**2 + ((i.y+i.speed) - (self.y-self.speed))**2)**(1/2) < 30:
                    mobs_t.append(i)
                elif i.side == 4 and ((i.x - self.x)**2 + (i.y - self.y)**2)**(1/2) < 30:
                    mobs_t.append(i)
        if self.side == 1:
            if self.level[posy][posx+1] == 0 and len(mobs_r) == 0:
                self.x += self.speed
            elif self.rect.right < (posx+1)*40 and len(mobs_r) == 0:
                self.x += self.speed
            else:
                self.side = random.choice([2, 3, 4])
        elif self.side == 2:
            if self.level[posy][posx-1] == 0 and len(mobs_l) == 0:
                self.x -= self.speed
            elif self.rect.left > (posx)*40 and len(mobs_l) == 0:
                self.x -= self.speed
            else:
                self.side = random.choice([1, 3, 4])
        elif self.side == 3:
            if self.level[posy+1][posx] == 0 and len(mobs_b) == 0:
                self.y += self.speed
            elif self.rect.bottom < (posy+1)*40 and len(mobs_b) == 0:
                self.y += self.speed
            else:
                self.side = random.choice([2, 1, 4])
        elif self.side == 4:
            if self.level[posy-1][posx] == 0 and len(mobs_t) == 0:
                self.y -= self.speed
            elif self.rect.top > (posy)*40 and len(mobs_t) == 0:
                self.y -= self.speed
            else:
                self.side = random.choice([2, 3, 1])
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def evade_arrow(self, graph, y, x):
        graph.pop((y, x), None)
        if (y, x+1) in graph:
            if (y, x) in graph[(y, x+1)]:
                graph[(y, x+1)
                      ].remove((y, x))

        if (y, x-1) in graph:
            if (y, x) in graph[(y, x-1)]:
                graph[(y, x-1)
                      ].remove((y, x))
        if (y-1, x) in graph:
            if (y, x) in graph[(y-1, x)]:
                graph[(y-1, x)
                      ].remove((y, x))
        if (y+1, x) in graph:
            if (y, x) in graph[(y+1, x)]:
                graph[(y+1, x)
                      ].remove((y, x))

    def blitme(self):
        self.screen.blit(self.image, self.rect)
