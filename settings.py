class Settings:

    def __init__(self):
        self.screen_width, self.screen_height = 1100, 600
        self.bg_color = (225, 100, 225)
        self.speed_factor = 2.5
        self.arrow_speed_factor = 5
        self.arrow_width = 16
        self.arrow_height = 16
        self.arrow_allowed = 1
        self.block_size = 40
        self.game_status = 0  # 0 - menu, 1 - game, 2 - dead
        self.score = 0
        self.current_lvl = 1
