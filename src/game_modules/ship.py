from pygame import Rect, Surface, image, constants
from pygame.event import Event


class Direction:
    def __init__(self, rect: Rect, screen_rect: Rect, axis: str, amount: int) -> None:
        self.rect = rect
        self.screen_rect = screen_rect
        self.amount = amount
        self.axis = axis

    def add(self):
        # if not self.check_screen():
        #     return
        if self.axis == 'x':
            self.rect.centerx += self.amount
        elif self.axis == 'y':
            self.rect.bottom += self.amount

    def check_screen(self):
        ok = True
        for check in [
            self.rect.left >= self.screen_rect.left,
            self.rect.right <= self.screen_rect.right,
            self.rect.bottom >= self.screen_rect.bottom,
            self.rect.top <= self.screen_rect.top
        ]:
            ok = check
        return ok


class ShipMovement:
    """handle ship movement"""

    def __init__(self, self_rect: Rect, screen_rect: Rect, x=0, y=0) -> None:
        self.rect = self_rect
        self.x = Direction(self.rect, screen_rect, 'x', x)
        self.y = Direction(self.rect, screen_rect, 'y', y)

        self.speed_multiplier = 1

        self.movement_dict = dict([
            (constants.K_UP, (self.y, -1)),
            (constants.K_DOWN, (self.y, 1)),
            (constants.K_LEFT, (self.x, -1)),
            (constants.K_RIGHT, (self.x, 1)),
        ])

    def event_listener(self, event: Event):
        """Listen to a pygame Event"""
        if event.type not in [constants.KEYUP, constants.KEYDOWN]:
            return
        if not event.key:
            return
        self.handle_shift(event)
        if not event.key in self.movement_dict:
            return
        direction, amount = self.movement_dict.get(event.key)

        if not direction:
            return
        if event.type == constants.KEYDOWN:
            direction.amount = amount * self.speed_multiplier
        elif event.type == constants.KEYUP:
            direction.amount = 0

    def handle_shift(self, event):
        print(event.key, constants.K_LSHIFT)
        if event.key == constants.K_LSHIFT:
            print("hit shift")
            if event.type == constants.KEYDOWN:
                self.set_speed_multiplier(4)
            else:
                self.set_speed_multiplier(1)

    def set_speed_multiplier(self, amount: int):
        self.speed_multiplier = amount

    def update(self):
        for direction in [self.x, self.y]:
            direction.add()


class Ship:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.image = image.load('src/images/ship.bmp')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.movement = ShipMovement(self.rect, self.screen_rect)

        # start ship at bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10

    def blit_me(self):
        """Draw ship at current location"""
        self.screen.blit(self.image, self.rect)
