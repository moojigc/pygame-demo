from typing import Literal, Tuple
from pygame import Rect, Surface, image, constants
from pygame.event import Event

from utils.settings import Settings


class Ship:
    def __init__(self, screen: Surface, game_settings: Settings) -> None:
        self.screen = screen
        self.image = image.load('src/images/ship.bmp')
        self.game_settings = game_settings

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start ship at bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10

        self.moving_x = 0
        self.moving_y = 0

        # store as float
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        self.speed_multiplier = 1

        # What key corresponds to what method
        self.movement_dict = dict([
            (constants.K_LEFT, lambda e: self.__set_direction_x(e, -1)),
            (constants.K_RIGHT, lambda e: self.__set_direction_x(e, 1)),
            (constants.K_UP, lambda e: self.__set_direction_y(e, -1)),
            (constants.K_DOWN, lambda e: self.__set_direction_y(e, 1)),
            (constants.K_LSHIFT, lambda e: self.__update_speed(e)),
            (constants.K_RSHIFT, lambda e: self.__update_speed(e))
        ])

        self.direction_dict = dict([
            (constants.KEYDOWN, 1),
            (constants.KEYUP, 0)
        ])

    def event_listener(self, event: Event):
        try:
            fn = self.movement_dict.get(event.key)
            if fn:
                fn(event)
        except AttributeError:
            pass

    def loop(self):
        """Draw ship at current location"""
        self.screen.blit(self.image, self.rect)
        self.__move()

    def __set_direction_x(self, event: Event, flag: Literal[-1, 0, 1]):
        self.moving_x = self.direction_dict.get(event.type) * flag

    def __set_direction_y(self, event: Event, flag: Literal[-1, 0, 1]):
        self.moving_y = self.direction_dict.get(event.type) * flag

    def __move(self):
        self.centerx += self.moving_x * self.__get_speed('x')
        self.rect.centerx = self.centerx
        self.bottom += self.moving_y * self.__get_speed('y')
        self.rect.bottom = self.bottom

    def __get_speed(self, dir):
        if not self.__check_screen()[dir]:
            return 0
        return self.game_settings.ship_speed * self.speed_multiplier

    def __check_screen(self):
        return {
            'x': self.rect.centerx >= self.screen_rect.x - 1,
            'y': self.rect.bottom >= self.screen_rect.y - 1
        }

    def __update_speed(self, e: Event):
        if e.type == constants.KEYDOWN:
            self.speed_multiplier = 4
        elif e.type == constants.KEYUP:
            self.speed_multiplier = 1
