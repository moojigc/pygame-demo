from pygame import display, init

from game_modules.ship import Ship
from game_modules.screen import Screen
from utils.event_watcher import EventWatcher
from utils.settings import Settings


class Game:
    """Main program"""
    @staticmethod
    def main():
        """Initialize game, paint screen"""
        settings = Settings()
        game = Game("Invaders from Python!", settings)
        game.run()

    # Instance

    def __init__(self, title: str, settings: Settings) -> None:
        self.screen = Screen(settings)
        self.title = title
        self.ship = Ship(self.screen.surface)
        self.event_watcher = EventWatcher(
            callbacks=[self.ship.movement.event_listener])
        self.__init_pygame()

    def run(self):
        """runs game loop"""
        while True:
            self.screen.loop()
            self.loop()

    def loop(self):
        # keyboard listener
        self.event_watcher.watch_pygame_events()
        self.ship.blit_me()
        self.ship.movement.update()
        display.flip()

    def __init_pygame(self):
        init()
        display.set_caption(self.title)
