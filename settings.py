class Settings:

    def __init__(self):
        self.screen_width, self.screen_height = 1100, 600
        self.bg_color = (225, 100, 225)
        self.speed_factor = 5
        self.arrow_speed_factor = 8
        self.arrow_width = 16
        self.arrow_height = 16
        self.arrow_allowed = 1
        self.block_size = 40
        self.game_status = 0  # 0 - menu, 1 - game, 2 - dead
        self.score = 0
        self.current_lvl = 1
        self.algorithm = 'bfs'
        self.time_dfs = '-'
        self.time_bfs = '-'
        self.time_ucs = '-'
        self.maps_dict = None
        self.key_dict = None
        self.exit_dict = None
        self.exit_coord = None
        self.key_coord = None
        self.last_v = [1, 2, 3]
        self.timer = 0
