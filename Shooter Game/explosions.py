from pygame.sprite import Sprite
from settings import Settings
import pygame


class Explosion(Sprite):
    """
    This class wil creates a grenade for our game
    """
    def __init__(self, x, y, scale):
        Sprite.__init__(self)
        self.settings = Settings()
        self.scale = scale
        self.x = x
        self.y = y
        self.images = []

        for i in range(1, 6):
            image = pygame.image.load(f'files/img/explosion/exp{i}.png')
            image = pygame.transform.scale(image, (int(image.get_width() * self.scale), int(image.get_height() * self.scale)))
            self.images.append(image)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, scroll):
        """
        Explodes th grenade and update the explosion images
        """
        self.rect.x += scroll
        explosion_speed = self.settings.explosion_speed

        self.counter += 1
        if self.counter >= explosion_speed:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]


if __name__ == '__main__':
    pass
