import copy


class Game:
    def __init__(self, map, mobs, player):
        self.state = []
        self.player_turn = 0
        self.mobs = mobs
        self.map = map
        self.player = player
        self.player_x = 0
        self.player_y = 0
        self.terminal = False
        self.mobs_coord = []

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

    def move(self, side):
        self.state = copy.deepcopy(self.map.tilemap1)
        for i in self.mobs:
            x = int(i.rect.centerx/40)
            y = int(i.rect.centery/40)
            self.state[y][x] == 13
        x = int(self.player.rect.centerx/40)
        y = int(self.player.rect.centery/40)
        if side == 1 and self.state[y][x-1] != 1:
            x -= 1
        elif side == 2 and self.state[y][x+1] != 1:
            x += 1
        elif side == 3 and self.state[y-1][x] != 1:
            y -= 1
        elif side == 4 and self.state[y+1][x] != 1:
            y += 1
        else:
            return False
        if self.state[y][x] == 9:
            self.terminal == True
        self.state[y][x] == 14
        self.player_x = x
        self.player_y = y
        return True

    def get_player_turn(self):
        return self.player_turn

    def is_terminal_state(self):
        if self.player.hp <= 0:
            return True
        if self.terminal:
            return True
        return False

    def end_game(self):
        pass
