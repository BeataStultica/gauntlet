import pygame


class Arrow(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, player):
        super().__init__()
        self.player = player
        self.side = self.player.side
        self.screen = screen
        self.sheet = pygame.image.load('assets/elf.png').convert()
        self.coords = {'left': (484, 350, 32, 32), 'right': (
            552, 350, 32, 32), 'up': (518, 350, 32, 32), 'down': (450, 350, 32, 32), 'topright': (535, 350, 32, 32),
            'topleft': (501, 350, 32, 32), 'bottomright': (569, 350, 32, 32),  'bottomleft': (467, 350, 32, 32)}

        self.rect = pygame.Rect(
            (0, 0, 16, 16))
        self.image = pygame.Surface(
            (ai_settings.arrow_width, ai_settings.arrow_height)).convert()
        self.image.blit(self.sheet, (0, 0), self.coords[self.player.side])
        self.transColor = self.image.get_at((0, 0))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect.centerx = self.player.x
        self.rect.centery = self.player.y
        #self.rect.top = player.rect.top
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        # self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.arrow_speed_factor

    def update(self):
        if self.side == 'right':
            self.x += self.speed_factor
            self.rect.x = self.x
        if self.side == 'left':
            self.x -= self.speed_factor
            self.rect.x = self.x
        if self.side == 'down':
            self.y += self.speed_factor
            self.rect.y = self.y
        if self.side == 'up':
            self.y -= self.speed_factor
            self.rect.y = self.y
        if self.side == 'topright':
            self.y -= self.speed_factor/1.414
            self.x += self.speed_factor/1.414
            self.rect.x = self.x
            self.rect.y = self.y
        if self.side == 'topleft':
            self.y -= self.speed_factor/1.414
            self.x -= self.speed_factor/1.414
            self.rect.x = self.x
            self.rect.y = self.y
        if self.side == 'bottomleft':
            self.y += self.speed_factor/1.414
            self.x -= self.speed_factor/1.414
            self.rect.x = self.x
            self.rect.y = self.y
        if self.side == 'bottomright':
            self.y += self.speed_factor/1.414
            self.x += self.speed_factor/1.414
            self.rect.x = self.x
            self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
