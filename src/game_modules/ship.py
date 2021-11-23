from typing import Literal, Tuple
from pygame import Rect, Surface, image, constants
from pygame.event import Event
from pygame.sprite import Group

from game_modules.bullet import Bullet
from utils.settings import Settings


class Ship:
    def __init__(self, screen: Surface, game_settings: Settings) -> None:
        self.screen = screen
        self.image = image.load('src/images/ship.bmp')
        self.bullets = Group()
        self.is_firing = False
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
            (constants.K_RSHIFT, lambda e: self.__update_speed(e)),
            (constants.K_SPACE, lambda e: self.set_is_firing(e))
        ])

        self.direction_dict = dict([
            (constants.KEYDOWN, 1),
            (constants.KEYUP, 0)
        ])

    def set_is_firing(self, event: Event):
        if event.type == constants.KEYDOWN:
            self.is_firing = True
        else:
            self.is_firing = False

    def fire_bullets(self):
        bullet_count = len(self.bullets.sprites())
        if self.is_firing and (not bullet_count or bullet_count % 3 != 0):
            bullet = Bullet(self.game_settings, self.screen, self)
            self.bullets.add(bullet)

    def event_listener(self, event: Event):
        try:
            fn = self.movement_dict.get(event.key)
            if fn:
                fn(event)
        except AttributeError:
            pass

    def loop(self):
        """Draw ship at current location"""
        self.fire_bullets()
        for bullet in self.bullets.sprites():
            if (bullet.is_off_screen()):
                self.bullets.remove(bullet)
            bullet.draw()
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
        flag: Literal[-1, 1]
        if dir == 'x':
            flag = (self.moving_x or 1) // abs(self.moving_x or 1)
        else:
            flag = (self.moving_y or 1) // abs(self.moving_y or 1)
        if not self.__check_screen()[dir][flag]:
            return 0
        return self.game_settings.ship_speed * self.speed_multiplier

    def __check_screen(self):
        return {
            'x': {
                -1: self.screen_rect.left <= self.rect.left,
                1: self.screen_rect.right >= self.rect.right
            },
            'y': {
                1: self.screen_rect.bottom >= self.rect.bottom,
                -1: self.screen_rect.height >= self.rect.top >= 0
            }
        }

    def __update_speed(self, e: Event):
        if e.type == constants.KEYDOWN:
            self.speed_multiplier = 4
        elif e.type == constants.KEYUP:
            self.speed_multiplier = 1
