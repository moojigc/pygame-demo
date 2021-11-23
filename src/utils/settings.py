class Settings:
    """Store game settings"""

    def __init__(self) -> None:
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen_tuple = (self.screen_width, self.screen_height)
        self.bg_color = (135, 206, 250)

        # ship settings
        self.ship_speed = 2

        # bullet settings
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
