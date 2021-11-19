from pygame import display
from game_modules.ship import Ship
from utils.settings import Settings


class Screen:
    def __init__(self, settings: Settings) -> None:
        self.x = settings.screen_width
        self.y = settings.screen_height
        self.bg_color = settings.bg_color
        self.surface = display.set_mode(settings.screen_tuple)

    def loop(self):
        self.surface.fill(self.bg_color)
