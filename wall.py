import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps, column, row):
        super().__init__()
        self.screen = screen
        self.maps = maps
        self.column = column
        self.row = row
        self.image = pygame.Surface(
            (20, 20)).convert()

        self.rect = self.image.get_rect()

        # self.image = pygame.Surface(
        # s    (20, 20)).convert()
        # self.image.blit(self.maps.textures_walls,
        #                (self.column*20, self.row*20), (0, 0, 20, 20))

        if self.row != len(self.maps.tilemap1)-1 and self.maps.tilemap1[self.row+1][self.column] == 0:
            self.image.blit(self.maps.textures_walls,
                            (0, 0), (0, 0, 20, 20))
        else:
            self.image.blit(self.maps.textures_walls,
                            (0, 0), (22, 0, 20, 20))
        self.rect.centerx = self.column*20
        self.rect.centery = self.row*20
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)
