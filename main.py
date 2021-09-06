import sys

import pygame

from player import Hero
from settings import Settings
import key_actions as k_a
from map import Map
from enemy import Enemy
from enemy_spawn import EnemySpawn


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
        self.all_sprites.add(self.player)
        self.maps = Map()
        self.mobs = pygame.sprite.Group()
        #self.mob = Enemy(self.settings, self.screen, self.maps)
        # self.mobs.add(self.mob)
        self.mobs_spawns = pygame.sprite.Group()
        pygame.display.set_caption("Gauntlet")

    def run_game(self):
        self.first_draw = 1
        while True:
            self.clock.tick(60)
            k_a.check_event(self.settings, self.screen,
                            self.player, self.arrows)
            k_a.update_screen(self.settings, self.screen,
                              self.player, self.all_sprites, self.arrows, self.maps, self.walls, self.mobs, self.mobs_spawns, self.first_draw)
            self.first_draw = 0


if __name__ == '__main__':
    game = GauntletGame()
    game.run_game()
