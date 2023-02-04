from soldier_character import Soldier
from bullets import Bullet
import pygame
import random


class Enemy(Soldier):
    """ Creates a player for the game """
    def __init__(self, x, y, scale, ammo, grenades, character_type, player):
        super().__init__(x, y, scale, ammo, grenades, character_type)
        self.moving = True
        self.action = 1
        self.player = player
        self.direction = 1
        self.flip = False
        self.idling_counter = 0
        self.vision_rect = pygame.rect.Rect(0, 0, 280, 20)
        self.bullet_group = pygame.sprite.Group()
        self.shoot_cooldown = self.setting.shoot_cooldown
        self.shoot_player = False
        self.damage_player = False
        self.jump_speed = self.setting.jump_speed
        self.shoot_sound = pygame.mixer.Sound('files/audio/shot.wav')

    def check_movement(self):
        """ Check if player dies or player standing or moving """
        if not self.moving or not self.player.alive:
            if self.alive:
                self.check_action(0)
            else:
                pass

    def update_animation(self):
        """Updates the character animation"""
        self.check_fire_cooldown()
        cooldown = 90
        self.check_movement()
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.last_update > cooldown:
            if self.frame_index == len(self.animation_list[self.action]) - 1:
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
            else:
                self.last_update = pygame.time.get_ticks()
                self.frame_index += 1

    def move(self, obstacles):
        """

        param left: This param takes the boolean value which mean player is moving left.
        param right: This param takes the boolean value which mean player is moving right.
        return:
        """
        dx = 0
        # dy = 0

        if self.moving and self.player.alive:
            if self.alive:
                dx = self.setting.enemy_speed * self.direction

        # for tile in obstacles:
        #     if tile[1].colliderect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()):
        #         dx = 0

            self.rect.x += dx
            # self.rect.y += dy

    def intelligence(self, screen, player, obstacle, scroll):
        """ - """
        if self.alive and self.player.alive:
            if random.randint(1, 200) == 1:
                self.moving = False
                self.idling_counter = 50

            if self.vision_rect.colliderect(player.rect):
                self.moving = False
                self.shoot_player = True
                self.start_shoot()
                self.draw_bullets(screen, obstacle)
                if pygame.sprite.spritecollide(player, self.bullet_group, True):
                    self.damage_player = True
                    self.damage_player_(player)

            else:
                if self.moving:
                    self.move_counter += 1
                    if self.move_counter >= self.setting.tile_size - 10:
                        self.direction *= -1
                        self.move_counter = 0
                        self.flip = True
                        if self.direction == 1:
                            self.flip = False
                    self.vision_rect.center = (self.rect.centerx + 150 * self.direction, self.rect.centery)
                    # pygame.draw.rect(screen, 'red', self.vision_rect)     # To check enemy's vision ('-')

                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.moving = True
                        self.check_action(1)

        self.rect.x += scroll

    def start_shoot(self):
        """ Enemy will start shooting after calling this function """
        if self.shoot_player:
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = self.setting.shoot_cooldown_b
                bullet = Bullet(self.rect.centerx + (33 * self.direction), self.rect.centery, self.direction)
                self.bullet_group.add(bullet)
                self.shoot_sound.play()
                self.ammo -= 1

    def draw_bullets(self, screen, obstacle_list):
        """ - """
        self.start_shoot()
        self.bullet_group.draw(screen)
        for bullet in self.bullet_group:
            bullet.update(obstacle_list)

    def check_fire_cooldown(self):
        """Check if shoot cooldown is > 0"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def damage_player_(self, player):
        """ - """
        if self.damage_player:
            player.health -= 8         # Jugadd --- need to repair later bug her ----------- Bug -------------
            self.damage_player = False


if __name__ == '__main__':
    pass
