import pygame


class Food(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps, column, row):
        super().__init__()
        self.screen = screen
        self.maps = maps
        self.column = column
        self.row = row
        self.block_size = ai_settings.block_size
        self.texture = pygame.image.load(
            'assets/gifts.png').convert()
        self.texture = pygame.transform.scale(
            self.texture, (159, 141))
        self.image = pygame.Surface(
            (self.block_size, self.block_size)).convert()

        self.rect = self.image.get_rect()
        self.image.blit(self.texture,
                        (0, 0), (0, 40, 40, 40))
        self.transColor = self.image.get_at((2, 2))
        self.image.set_colorkey(self.transColor)
        self.rect.centerx = self.column*self.block_size
        self.rect.centery = self.row*self.block_size
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery
        self.value = 400

    def blitme(self):
        self.screen.blit(self.image, self.rect)
