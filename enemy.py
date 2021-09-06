import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.ai_settings = ai_settings
        self.block_size = ai_settings.block_size
        self.sheet = pygame.image.load('assets/ghost.png').convert()
        self.sheet = pygame.transform.scale(
            self.sheet, (12*self.block_size, 8*self.block_size))
        #self.image = None
        self.rect = pygame.Rect((0, 0, self.block_size, self.block_size))
        self.image = pygame.Surface(
            (self.block_size, self.block_size)).convert()
        self.image.blit(self.sheet, (0, 0), self.rect)
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        self.side = 'right'
        self.hp = 10
        self.atk = 100

    def update(self):
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.speed_factor * \
                self.speed_factor_collise[1]
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.ai_settings.speed_factor * \
                self.speed_factor_collise[0]
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.speed_factor * \
                self.speed_factor_collise[3]
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.ai_settings.speed_factor * \
                self.speed_factor_collise[2]
        """

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)