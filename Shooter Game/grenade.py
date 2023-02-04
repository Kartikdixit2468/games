from pygame.sprite import Sprite
from settings import Settings
from explosions import Explosion
import pygame


class Grenade(Sprite):
    """
    This class wil creates a grenade for our game
    """
    def __init__(self, x, y, direction):
        Sprite.__init__(self)
        self.settings = Settings()
        self.timer = 50
        self.x = x
        self.y = y
        self.image = pygame.image.load('files/img/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = self.settings.grenade_speed
        self.vel_y = self.settings.grenade_y_speed
        self.tile_size = self.settings.tile_size
        self.effect = True
        self.grenade_sound = pygame.mixer.Sound('files/audio/grenade.wav')

    def update(self, group, char, enemy_group, obstacle_list, scroll):
        """ Updated the grenades position """

        self.rect.x += scroll
        self.vel_y += self.settings.gravity
        x = self.speed * self.direction
        y = self.vel_y

        for tile in obstacle_list:

            if tile[1].colliderect(self.rect.x + x, self.y , self.image.get_width(), self.image.get_height()):
                self.direction *= -1
                x = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + y, self.image.get_width(), self.image.get_height()):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    y = tile[1].bottom - self.rect.top
                elif self.vel_y > 0:
                    self.vel_y = 0
                    y = tile[1].top - self.rect.bottom

        if self.rect.right + x < 0 or self.rect.left + x > self.settings.screen_width:
            self.direction *= -1
            x = self.direction * self.speed

        # Position Updated
        self.rect.x += x
        self.rect.y += y

        self.timer -= 1

        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            group.add(explosion)
            self.grenade_sound.play()

            if abs(self.rect.centerx - char.rect.centerx) < self.tile_size * 2 and abs(self.rect.centery - char.rect.centery) < self.tile_size * 2:
                char.health -= 200
                if char.health <= 0:
                    char.health = 0

            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < self.tile_size * 2 and abs(self.rect.centery - enemy.rect.centery) < self.tile_size * 2:
                    enemy.health -= 200
                    if enemy.health <= 0:
                        enemy.health = 0


if __name__ == '__main__':
    pass
