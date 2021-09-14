import pygame


class Key(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps, column, row):
        super().__init__()
        self.screen = screen
        self.maps = maps
        self.column = column
        self.row = row
        self.block_size = ai_settings.block_size
        self.texture = pygame.image.load(
            'assets/key.png').convert()
        self.image = pygame.Surface(
            (self.block_size, self.block_size)).convert()

        self.rect = self.image.get_rect()
        self.image.blit(self.texture,
                        (0, 0))
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.rect.centerx = self.column*self.block_size
        self.rect.centery = self.row*self.block_size
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)
