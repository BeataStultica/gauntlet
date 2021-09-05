import sys

import pygame

from player import Hero
from settings import Settings
import key_actions as k_a


class GauntletGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.player = Hero(self.settings, self.screen)
        self.all_sprites.add(self.player)
        pygame.display.set_caption("Gauntlet")

    def run_game(self):
        while True:
            self.clock.tick(60)
            k_a.check_event(self.settings, self.screen, self.player)
            k_a.update_screen(self.settings, self.screen,
                              self.player, self.all_sprites)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = GauntletGame()
    game.run_game()
