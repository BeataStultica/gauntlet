import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps, column, row):
        super().__init__()
        self.screen = screen
        self.maps = maps
        self.lvl = self.maps.levels[ai_settings.current_lvl]
        self.column = column
        self.row = row
        self.block_size = ai_settings.block_size
        self.image = pygame.Surface(
            (self.block_size, self.block_size)).convert()

        self.rect = self.image.get_rect()

        if self.row != len(self.lvl)-1 and self.lvl[self.row+1][self.column] != 1:
            self.image.blit(self.maps.textures_walls,
                            (0, 0), (0, 0, self.block_size, self.block_size))
        else:
            self.image.blit(self.maps.textures_walls,
                            (0, 0), (44, 0, self.block_size, self.block_size))
        self.rect.centerx = self.column*self.block_size
        self.rect.centery = self.row*self.block_size
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)
