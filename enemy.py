import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, x, y, maps):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
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
        self.side = 2
        self.hp = 10
        self.atk = 200
        self.speed = 1
        self.cost = 10

    def update(self):
        posy = int(self.rect.centery/self.block_size)
        posx = int(self.rect.centerx/self.block_size)
        if self.side == 1:
            if self.level[posy][posx+1] == 0:
                self.x += self.speed
            elif self.rect.right < (posx+1)*40:
                self.x += self.speed
            else:
                self.side = random.choice([2, 3, 4])
        elif self.side == 2:
            if self.level[posy][posx-1] == 0:
                self.x -= self.speed
            elif self.rect.left > (posx)*40:
                self.x -= self.speed
            else:
                self.side = random.choice([1, 3, 4])
        elif self.side == 3:
            if self.level[posy+1][posx] == 0:
                self.y += self.speed
            elif self.rect.bottom < (posy+1)*40:
                self.y += self.speed
            else:
                self.side = random.choice([2, 1, 4])
        else:
            if self.level[posy-1][posx] == 0:
                self.y -= self.speed
            elif self.rect.top > (posy)*40:
                self.y -= self.speed
            else:
                self.side = random.choice([2, 3, 1])
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
