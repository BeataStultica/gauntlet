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
        self.all_sprites.add(self.player)
        self.maps = Map()
        self.mobs = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.mobs_spawns = pygame.sprite.Group()
        self.treasure = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.lvl = 1
        pygame.display.set_caption("Gauntlet")

    def clean_after_dead(self):
        for i in self.walls:
            i.kill()
        for i in self.mobs:
            i.kill()
        for i in self.exits:
            i.kill()
        for i in self.mobs_spawns:
            i.kill()
        for i in self.treasure:
            i.kill()
        for i in self.foods:
            i.kill()

    def new_game(self):
        self.lvl = 1
        self.maps = Map()
        for i in self.all_sprites:
            i.kill()
        self.player = Hero(self.settings, self.screen)
        self.all_sprites.add(self.player)

    def run_game(self):
        self.first_draw = 1
        while True:
            self.clock.tick(60)
            k_a.check_game_event(self.settings, self.screen,
                                 self.player, self.arrows)
            if self.settings.game_status == 0:
                k_a.draw_menu_screen(self.screen,  self.settings)
                self.clean_after_dead()
                self.new_game()
                self.first_draw = 1
            elif self.settings.game_status == 1:
                k_a.update_screen(self.settings, self.screen,
                                  self.player, self.all_sprites, self.arrows, self.maps, self.walls, self.mobs, self.mobs_spawns, self.exits, self.treasure, self.foods, self.first_draw)
                if self.lvl == self.settings.current_lvl:
                    self.first_draw = 0
                else:
                    self.first_draw = 1
                    self.lvl += 1
                    if self.lvl == 4:
                        self.settings.game_status = 3
                        self.settings.current_lvl = 1
                    self.clean_after_dead()
            elif self.settings.game_status == 2:
                k_a.draw_end_screen(self.screen,  self.settings)
                self.clean_after_dead()
                self.new_game()
                self.first_draw = 1
            elif self.settings.game_status == 3:
                k_a.draw_win_screen(self.screen,  self.settings)
                self.clean_after_dead()
                self.new_game()
                self.first_draw = 1


if __name__ == '__main__':
    game = GauntletGame()
    game.run_game()
