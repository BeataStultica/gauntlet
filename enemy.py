import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, x, y, maps, mobs):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.mobs = mobs
        self.level = maps.tilemap1
        self.ai_settings = ai_settings
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
        self.speed = 1
        self.cost = 10

    def update(self):
        posy = int(self.rect.centery/self.block_size)
        posx = int(self.rect.centerx/self.block_size)
        mobs_l = []
        mobs_r = []
        mobs_t = []
        mobs_b = []
        for i in self.mobs:
            if i == self:
                continue
            curr_d = ((i.x - self.x)**2 + (i.y - self.y)**2)**(1/2)
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

    def blitme(self):
        self.screen.blit(self.image, self.rect)
