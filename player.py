import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.sheet = pygame.image.load('assets/elf.png').convert()
        self.ai_settings = ai_settings
        #self.image = None
        self.rect = pygame.Rect((450, 75, 48, 48))
        self.image = pygame.Surface((24, 24)).convert()
        self.image.blit(self.sheet, (0, 0), self.rect)
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.ai_settings.speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.ai_settings.speed_factor
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
