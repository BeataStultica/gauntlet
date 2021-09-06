import pygame


class EnemySpawn(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps, column, row):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.sheet = pygame.image.load('assets/spawn_ghost.png').convert()
        self.ai_settings = ai_settings
        self.image = pygame.Surface((25, 40)).convert()
        self.sheet = pygame.transform.scale(self.sheet, (25, 40))
        self.rect = self.image.get_rect()
        self.image.blit(self.sheet, (0, 0))
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.screen_rect = screen.get_rect()
        self.rect.x = column*40
        self.rect.y = row*40
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

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
