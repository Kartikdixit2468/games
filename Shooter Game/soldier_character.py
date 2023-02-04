# Made by Kartik
import pygame
from settings import Settings


class Soldier(pygame.sprite.Sprite):
    """The main game player in here"""
    def __init__(self, x, y, scale, ammo, grenades, character_type):
        """It initializes the main game function and variables,
        Main class constructor
         """
        pygame.init()
        pygame.sprite.Sprite.__init__(self)  # Inherits Sprite from pygame, As -> Super().__init__(self):
        self.ammo = ammo
        self.grenades = grenades
        self.alive = True
        self.jump = False
        self.character_type = str(character_type).lower()
        self.scale = scale
        self.setting = Settings()
        self.jump_speed = self.setting.jump_speed
        # self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        self.animation_list = []
        self.frame_index = 0
        self.temp_list = []
        self.action = 0  # 0 = standing & 1 = running, 2 = jumping,
        self.last_update = pygame.time.get_ticks()
        self.animation_type = ['idle', 'run', 'jump']

        for j in self.animation_type:
            if j != 'jump':
                for i in range(0, 5):
                    image = pygame.image.load(f'./files/img/{self.character_type}/{j}/{i}.png')
                    image = pygame.transform.scale(image, (
                                                            int(image.get_width() * self.scale), int(image.get_height() * self.scale)))
                    self.temp_list.append(image)
            else:
                image = pygame.image.load(f'./files/img/{self.character_type}/{j}/0.png')
                image = pygame.transform.scale(image, (
                                                        int(image.get_width() * self.scale), int(image.get_height() * self.scale)))
                self.temp_list.append(image)

            self.animation_list.append(self.temp_list)
            self.temp_list = []

        for i in range(0, 7):
            image = pygame.image.load(f'./files/img/{self.character_type}/death/{i}.png')
            image = pygame.transform.scale(image, (
                                                    int(image.get_width() * self.scale), int(image.get_height() * self.scale)))
            self.temp_list.append(image)
        self.animation_list.append(self.temp_list)
        self.temp_list = []

        # self.img = self.animation_list[self.action][self.frame_index]
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.moving_left = False
        self.moving_right = False
        self.movement = True

        self.flip = False
        self.direction = 1
        self.in_air = False
        self.max_health = self.setting.max_health
        self.health = self.setting.health
        self.y_speed = self.setting.p_y_speed

        # Intelligence Variables
        self.move_counter = 0

    def update_animation(self):
        """Updates the character animation"""
        cooldown = 90
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
            if self.jump:
                self.check_action(2)

    def draw_character(self, screen):
        """This function draws the player on the game screen"""
        return screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def check_action(self, new_action):
        """This function checks for change in action of player
        1 for running
        0 for standing
        """
        self.frame_index = 0
        self.action = new_action

    def check_alive(self):
        """
        Changes character animation for death.
        Check player if alive
        """
        if self.alive:
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.check_action(3)
                self.movement = False
                self.moving_right = False
                self.moving_left = False
                self.setting.p_speed = 0


if __name__ == '__main__':
    pass
