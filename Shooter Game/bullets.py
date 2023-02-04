from settings import Settings
from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """ Creates bullet instance of our game """
    def __init__(self, x, y, direction):
        """
        Initializes the bullet class
        :param x:
        :param y:
        :param direction:
        """
        Sprite.__init__(self)
        self.settings = Settings()
        self.image = pygame.image.load('files/img/icons/bullet.png').convert_alpha()
        self.bullet_speed = self.settings.bullet_speed
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.countdown = 20

    def update(self, obstacle_list):
        """Updates the position of the bullets"""
        self.rect.x += (self.settings.bullet_speed * self.direction)

        if self.rect.right < 0 or self.rect.left > self.settings.screen_width + 1:
            self.kill()
        for tile in obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()


if __name__ == '__main__':
    pass
