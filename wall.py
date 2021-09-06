import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, maps, column, row):
        super().__init__()
        self.screen = screen
        self.maps = maps
        self.column = column
        self.row = row
        self.rect = pygame.Rect((self.column*20, self.row*20, 20, 20)
                                )
        self.image = pygame.Surface(
            (20, 20)).convert()
        if self.row != len(self.maps.tilemap1)-1 and self.maps.tilemap1[self.row+1][self.column] == 0:
            self.image.blit(self.maps.textures_walls,
                            (self.column*20, self.row*20), (0, 0, 20, 20))
        else:
            self.image.blit(self.maps.textures_walls,
                            (self.column*20, self.row*20), (22, 0, 20, 20))
