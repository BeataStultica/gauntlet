import sys

import pygame

from player import Hero
from settings import Settings
import key_actions as k_a
from map import Map


class GauntletGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.player = Hero(self.settings, self.screen)
        self.maps = Map()
        self.all_sprites.add(self.player)
        pygame.display.set_caption("Gauntlet")

    def run_game(self):
        while True:
            self.clock.tick(60)
            k_a.check_event(self.settings, self.screen,
                            self.player, self.arrows)
            k_a.update_screen(self.settings, self.screen,
                              self.player, self.all_sprites, self.arrows, self.maps, self.walls)

    def _update_screen(self):
        for row in range(len(self.maps.tilemap)):
            for column in range(len(self.maps.tilemap[0])):
                self.screen.blit(self.maps.textures_floor,
                                 (column*20, row*20), (0, 0, 60, 60))
        self.screen.update()
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = GauntletGame()
    game.run_game()
