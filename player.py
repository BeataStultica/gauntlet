import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.sheet = pygame.image.load('assets/elf.png').convert()
        self.sheet = pygame.transform.scale(
            self.sheet, (1198, 832))
        self.ai_settings = ai_settings
        self.block_size = self.ai_settings.block_size
        self.rect = pygame.Rect((450, 75, 38, 38))
        self.image = pygame.Surface((49, 49)).convert()
        self.image.blit(self.sheet, (0, 0), (900, 150, 50, 50))
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.scale(
            self.image, (40, 40))
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        self.speed_factor_collise = [1, 1, 1, 1]  # left right, top, bottom
        self.side = 'right'
        self.atk = 10
        self.max_hp = 1000
        self.hp = 1000
        self.score = 0
        self.keys = 0
        self.mobs_limit = 2
        self.mobs_random_limit = 0

    def update(self):
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
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
