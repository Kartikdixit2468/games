import pygame.image

from settings import Settings
from pygame.sprite import Sprite


class ItemBox(Sprite):
    """
    This class wil creates an item box on our game screen
    """
    def __init__(self, x, y, item_type):
        """
        Class constructor __init__
        :param x: x coordinate of item box
        :param y: y coordinate of item box
        :param item_type: It indicates box type. -> Health, Ammo, Grenade
        """
        Sprite.__init__(self)
        self.health_box = pygame.image.load('files/img/icons/health_box.png').convert_alpha()
        self.ammo_box = pygame.image.load('files/img/icons/ammo_box.png').convert_alpha()
        self.grenade_box = pygame.image.load('files/img/icons/grenade_box.png').convert_alpha()
        self.item_boxes = {
            'Health': self.health_box,
            'Ammo': self.ammo_box,
            'Grenade': self.grenade_box
        }
        self.item_type = item_type
        self.settings = Settings()
        self.image = self.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + (self.settings.tile_size // 2), y + (self.settings.tile_size - self.image.get_height()))

    def update(self, player, scroll):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                if player.health >= player.max_health:
                    player.health = 100
                else:
                    player.health += 30
            if self.item_type == 'Ammo':
                player.ammo += 10
            if self.item_type == 'Grenade':
                player.grenades += 5
            self.kill()

        self.rect.x += scroll


if __name__ == '__main__':
    pass
