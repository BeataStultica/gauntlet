import copy


class Game:
    def __init__(self, map, mobs, player):
        self.state = copy.deepcopy(map.tilemap1)
        self.player_turn = 0
        self.mobs = mobs
        self.map = map
        self.player = player
        self.terminal = False

    def get_state(self):
        return copy.deepcopy(self.state)

    def update_map(self):
        self.state = copy.deepcopy(self.map.tilemap1)
        for i in self.mobs:
            x = int(i.rect.centerx/40)
            y = int(i.rect.centery/40)
            self.state[y][x] == 13
        x = int(self.player.rect.centerx/40)
        y = int(self.player.rect.centery/40)
        if self.state[y][x] == 9:
            self.terminal == True
        self.state[y][x] == 14

    def get_player_turn(self):
        return self.player_turn

    def take_slot(self, pocket):
        pass

    def is_terminal_state(self):
        if self.player.hp <= 0:
            return True
        if self.terminal:
            return True
        return False

    def end_game(self):
        pass
