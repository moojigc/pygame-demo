from pygame.sprite import Sprite
from utils.settings import Settings
from pygame import Rect, Surface, draw


class Bullet(Sprite):
    """Ze bullets fired from ze ship."""

    def __init__(self, settings: Settings, screen: Surface, ship) -> None:
        super(Bullet, self).__init__()
        self.screen = screen

        # init position
        self.rect = Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store bullet's pos as float
        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        """move bullet"""
        # update decimal pos
        self.y -= self.speed
        # update rect
        self.rect.y = self.y

    def draw(self):
        """draw to screen"""
        draw.rect(self.screen, self.color, self.rect)
        self.update()

    def is_off_screen(self):
        return self.rect.bottom <= 0
