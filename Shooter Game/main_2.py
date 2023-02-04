# Made by Kartik
from enemy import Enemy
from soldier_character import Soldier
from health_bar import HealthBar
from settings import Settings
from item_box import ItemBox
from grenade import Grenade
from bullets import Bullet
import pygame
import csv

pygame.init()
decoration_group = []
water_group = []
exit_group = []
new_y = 0


class Main:
    """It manages the main game"""

    def __init__(self):
        """It initializes the main game function and variables,
        Main class constructor
         """
        pygame.init()
        # Settings class
        self.settings = Settings()
        self.screen = pygame.display
        self.main_screen = self.screen.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(" Enemy Shooter | Made by Kartik ")
        # self.main_screen.fill("white")

        # Map
        self.map = Map()
        self.map.process_data()
        self.game_data = self.map.return_data()

        self.player = self.game_data[0]

        # Created a player
        # self.player = Soldier(self.settings.p_x, self.settings.p_y, self.settings.p_scale, 'player')
        # self.player = Soldier(self.settings.p_x, self.settings.p_y, self.settings.p_scale, self.settings.p_ammo, self.settings.p_grenades, 'player')

        self.moving_left = self.player.moving_left
        self.moving_right = self.player.moving_right

        # Created an enemy and enemy group

        self.enemy_group = self.game_data[2]

        # enemy = Enemy(self.settings.enemy_x, self.settings.enemy_y, self.settings.enemy_scale, self.settings.e_ammo, self.settings.e_grenades, 'enemy', self.player)
        # enemy_2 = Enemy(self.settings.enemy_x + 400, self.settings.enemy_y, self.settings.enemy_scale, self.settings.e_ammo, self.settings.e_grenades, 'enemy', self.player)
        # self.enemy_group = pygame.sprite.Group()
        # self.enemy_group.add(enemy)
        # self.enemy_group.add(enemy_2)

        # Health Bar
        # self.health_bar = HealthBar(10, 20, self.player.health, self.player.max_health)
        self.health_bar = self.game_data[1]

        # Bullet group
        self.bullet_group = pygame.sprite.Group()
        self.shoot = False

        # Grenade group
        self.grenade_group = pygame.sprite.Group()
        self.fire_grenade = False
        self.g_thrown = True

        # Item Boxes
        # self.item_box_group = pygame.sprite.Group()
        self.item_box_group = self.game_data[3]

        # self.item_box_1 = ItemBox(250, 412, 'Health')
        # self.item_box_2 = ItemBox(650, 412, 'Grenade')
        # self.item_box_3 = ItemBox(800, 412, 'Ammo')
        # self.item_box_group.add(self.item_box_1)
        # self.item_box_group.add(self.item_box_2)
        # self.item_box_group.add(self.item_box_3)

        # Game sensitivity (Clock) and fps
        self.clock = pygame.time.Clock()

        # Game Variables
        self.run = True
        self.gravity = self.settings.gravity
        self.jump_speed = self.settings.jump_speed

        #  Explosion
        self.explosion_group = pygame.sprite.Group()

        # Bullet firing settings
        self.shoot_cooldown = self.settings.shoot_cooldown

        # Font
        self.font = pygame.font.SysFont('Futura', 30)

        # Colours
        self.c_white = (255, 255, 255)

        # Decorations and Water
        # self.decoration_group = self.game_data[4]
        # self.water_group = self.game_data[5]
        # self.exit_group = self.game_data[6]

    def main(self):
        """This function contains the main loop of the game and runs the game"""
        global exit_group, water_group, decoration_group
        while self.run:
            self.clock.tick(self.settings.fps)
            self.draw_bg()
            self.map.draw(self.main_screen)
            self.blit_instances()
            self.update_char_animation()
            self.check_fire_cooldown()
            self.check_enemy_movement()
            self.check_player_movement()
            self.enemy_group_draw(self.main_screen)
            self.player.draw_character(self.main_screen)
            self.bullet_group.draw(self.main_screen)
            self.grenade_group.draw(self.main_screen)
            self.explosion_group.draw(self.main_screen)
            self.item_box_group.draw(self.main_screen)
            self.bullet_group.update()
            self.grenade_group.update(self.explosion_group, self.player, self.enemy_group)
            self.explosion_group.update()
            self.update_item_boxes()
            self.check_collision()
            self.check_char_alive()
            self.check_events_2()
            pygame.display.update()

    def enemy_group_draw(self, screen):
        """ - """
        for enemy in self.enemy_group:
            enemy.draw_character(screen)

    def blit_instances(self):
        """It draws the score, bullets, grenades etc"""
        bullet_img = pygame.image.load('files/img/icons/bullet.png').convert_alpha()
        grenade_img = pygame.image.load('files/img/icons/grenade.png').convert_alpha()

        self.health_bar.draw_health_bar(self.main_screen, self.player.health)
        self.draw_text('AMMO: ', self.font, self.c_white, 10, 50)
        self.draw_text('GRENADES: ', self.font, self.c_white, 10, 70)
        for i in range(self.player.ammo):
            self.main_screen.blit(bullet_img, (90 + (i * 10), 50))
        for i in range(self.player.grenades):
            self.main_screen.blit(grenade_img, (150 + (i * 15), 70))

    def draw_text(self, text, font, color, x, y):
        """ Draws text on screen"""
        img = font.render(text, True, color)
        self.main_screen.blit(img, (x, y))

    def update_item_boxes(self):
        """ Updates the item box and call the box.update() function"""
        for box in self.item_box_group:
            box.update(self.player)

    def update_char_animation(self):
        """ Update the enemy animation """
        self.player.update_animation()
        for enemy in self.enemy_group:
            enemy.update_animation()

    def check_char_alive(self):
        """ Check if the enemy is dead or live """
        for enemy in self.enemy_group:
            enemy.check_alive()

        self.player.check_alive()

    def check_collision(self):
        """Check if soldier or bullets collides to each other """
        delete_bullet = False
        for enemy in self.enemy_group:
            if enemy.alive:
                delete_bullet = True

            elif not enemy.alive:
                delete_bullet = False

            if pygame.sprite.spritecollide(enemy, self.bullet_group, delete_bullet):
                enemy.health -= 20

    def check_fire_cooldown(self):
        """Check if shoot cooldown is > 0"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw_bg(self):
        """Fills background color and makes a line"""
        self.main_screen.fill(self.settings.bg_color)
        pygame.draw.line(self.main_screen, 'red', (0, 450), (1200, 450))

    def check_events(self):
        """Check for the instructions gives by keyboard from user"""
        self.clock.tick(self.settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.quit():
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()

    def check_events_2(self):
        """Check for the instruction gives by keyboard from user"""
        event = pygame.event.poll()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.run = False

            if event.key == pygame.K_UP and self.player.alive:
                self.player.jump = True
                # self.player.check_action(2)

            if self.player.alive:

                if event.key == pygame.K_RIGHT:
                    self.moving_right = True
                    self.moving_left = False
                    self.player.check_action(1)

                elif event.key == pygame.K_LEFT:
                    self.moving_left = True
                    self.moving_right = False
                    self.player.check_action(1)

                if event.key == pygame.K_s:
                    self.shoot = True

                if event.key == pygame.K_x:
                    self.fire_grenade = True
                    self.g_thrown = False

        elif event.type == pygame.KEYUP:

            if self.player.alive:

                if event.key == pygame.K_RIGHT and not self.moving_left:
                    self.moving_right = False
                    self.player.check_action(0)

                elif event.key == pygame.K_LEFT and not self.moving_right:
                    self.moving_left = False
                    self.player.check_action(0)

                if event.key == pygame.K_UP:
                    if self.moving_left or self.moving_right:
                        self.player.check_action(1)
                    else:
                        self.player.check_action(0)

                if event.key == pygame.K_s:
                    self.shoot = False

                if event.key == pygame.K_x:
                    self.fire_grenade = False

        elif event.type == pygame.QUIT:
            self.run = False

    def shoot_bullets(self):
        """
        Creates the bullet class and fire them
        :return bullet:
        """
        if self.shoot_cooldown == 0 and self.player.ammo > 0:
            self.shoot_cooldown = 18
            bullet = Bullet(self.player.rect.centerx + (33 * self.player.direction), self.player.rect.centery,
                            self.player.direction)
            self.bullet_group.add(bullet)
            self.player.ammo -= 1

    def check_enemy_movement(self):
        """ This function manages the movement of enemy in our game """
        for enemy in self.enemy_group:
            enemy.move()
            enemy.intelligence(self.main_screen, self.player)

    def check_player_movement(self):
        """This function makes our game player move"""

        global new_y
        if self.player.alive:

            if self.fire_grenade and not self.g_thrown and self.player.grenades > 0:
                grenade = Grenade(self.player.rect.centerx + (0.5 * self.player.rect.size[0] * self.player.direction),
                                  self.player.rect.top, self.player.direction)
                self.grenade_group.add(grenade)
                self.g_thrown = True
                self.player.grenades -= 1

            if self.shoot:
                self.shoot_bullets()
                self.shoot = False

            if self.moving_right:
                self.player.rect.x += self.settings.p_speed
                self.player.flip = False
                self.player.direction = 1

            elif self.moving_left:
                self.player.rect.x -= self.settings.p_speed
                self.player.flip = True
                self.player.direction = -1

            if self.player.jump:
                self.player.rect.y += self.jump_speed
                self.jump_speed += self.settings.gravity
                self.player.in_air = True

                if self.player.rect.y >= new_y:
                    self.player.jump = False
                    self.player.in_air = False
                    self.jump_speed = self.settings.jump_speed
                    if self.moving_right or self.moving_left:
                        self.player.check_action(1)
                    else:
                        self.player.check_action(0)

    def quit_game(self):
        """This function ask the user to continue if he/she is sure to quit the game
        It makes a pop-up window
        """
        pass


class Map:
    """ It creates the map of our game """

    def __init__(self):
        """
         -> __init__ class constructor contains the class variable
        Also initializes the class components

        Data -:
            Tile no. 0 - 8 = Obstacles
            Tile no. 9 - 10 = Water
            Tile no. 11 - 14 = Decoration
            Tile no. 15 = Player
            Tile no. 16 = Enemy
            Tile no. 17 = Ammo Box
            Tile no. 18 = Grenade Box
            Tile no. 19 = Health Box
            Tile no. 20 = Exit
        """
        self.player_var = []
        self.settings = Settings()
        self.tile_types = self.settings.tile_types
        self.rows = self.settings.rows
        self.columns = self.settings.columns
        # self.tile_size = self.settings.screen_height // self.rows
        self.item_box_group = pygame.sprite.Group()
        self.tile_size = 50
        self.level = 1
        self.y_add = self.settings.y_additional_space
        self.obstacles = []
        self.images = []
        self.enemy_group = pygame.sprite.Group()
        # self.decoration_group = pygame.sprite.Group()
        # self.water_group = pygame.sprite.Group()
        # self.exit_group = pygame.sprite.Group()

        for i in range(0, self.tile_types):
            img = pygame.image.load(f'files/img/tile/{i}.png')
            img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            self.images.append(img)
        self.world_data = []

        for i in range(self.rows):
            r = [-1] * self.columns
            self.world_data.append(r)

    def process_data(self):
        """
        Takes data and convert it into a map
        Tile by tile -
        :return: map
        """
        global exit_group, water_group, decoration_group, new_y

        with open(f'csv/level{self.level}_data.csv', mode='r', newline='') as map_file:
            reader = csv.reader(map_file, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    image = self.images[tile]
                    rect = image.get_rect()
                    rect.x = x * self.tile_size
                    rect.y = y * self.tile_size
                    tile_data = (image, rect)
                    # self.obstacles.append(tile_data)

                    if 0 <= tile <= 8:
                        self.obstacles.append(tile_data)

                    elif 9 <= tile <= 10:
                        # self.obstacles.append(tile_data)
                        water = Water(image, x, y)
                        water_group.append(water)

                    elif 11 <= tile <= 14:
                        # self.obstacles.append(tile_data)
                        decorations = Decoration(image, x * self.tile_size, y * self.tile_size + self.y_add)
                        decoration_group.append(decorations)

                    elif tile == 15:

                        # player = Soldier(self.settings.p_x, self.settings.p_y, self.settings.p_scale,
                        #                  self.settings.p_ammo, self.settings.p_grenades, 'player')
                        new_y = y * self.tile_size + self.y_add
                        player = Soldier(x * self.tile_size, y * self.tile_size + self.y_add, self.settings.p_scale,
                                         self.settings.p_ammo, self.settings.p_grenades, 'player')
                        # Health Bar
                        health_bar = HealthBar(10, 20, player.health, player.max_health)
                        self.player_var.append(player)
                        self.player_var.append(health_bar)

                    elif tile == 17:
                        item_box_1 = ItemBox(x * self.tile_size, y * self.tile_size + self.y_add - 10, 'Health')
                        self.item_box_group.add(item_box_1)

                    elif tile == 18:
                        item_box_2 = ItemBox(x * self.tile_size, y * self.tile_size + self.y_add - 10, 'Grenade')
                        self.item_box_group.add(item_box_2)

                    elif tile == 19:
                        item_box_3 = ItemBox(x * self.tile_size, y * self.tile_size + self.y_add - 10, 'Ammo')
                        self.item_box_group.add(item_box_3)

                    elif tile == 20:
                        # self.obstacles.append(tile_data)
                        _exit = Exit(image, x * self.tile_size, y * self.tile_size + self.y_add)
                        exit_group.append(_exit)

        for y_, row_ in enumerate(self.world_data):
            for x_, tile in enumerate(row_):
                if tile == 16:
                    # enemy = Enemy(self.settings.enemy_x, self.settings.enemy_y, self.settings.enemy_scale,
                    #               self.settings.e_ammo, self.settings.e_grenades, 'enemy', self.player_var[0])
                    # self.enemy_group.add(enemy)
                    enemy = Enemy(x_ * self.tile_size, y_ * self.tile_size + self.y_add, self.settings.enemy_scale,
                                  self.settings.e_ammo, self.settings.e_grenades, 'enemy', self.player_var[0])
                    self.enemy_group.add(enemy)
                else:
                    continue

    def return_data(self):
        """
        Return data in a list form from raw data
        Tile by tile -
        :return: A list containing player, health bar, enemy group, item box group
        """

        return [self.player_var[0], self.player_var[1], self.enemy_group, self.item_box_group]

    def draw(self, screen):
        """ Draws the mapon the screen """
        for tile in self.obstacles:
            screen.blit(tile[0], tile[1])

        for sprite in exit_group:
            sprite.draw(screen)

        for sprite in water_group:
            sprite.draw(screen)

        for sprite in decoration_group:
            sprite.draw(screen)


class Water(pygame.sprite.Sprite):
    """ - """

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x * self.settings.tile_size // 2, y * (self.settings.tile_size - self.image.get_height()))

    def draw(self, screen):
        """ - """
        screen.blit(self.image, self.rect)


class Exit(pygame.sprite.Sprite):
    """ - """

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x * self.settings.tile_size // 2, y * (self.settings.tile_size - self.image.get_height()))

    def draw(self, screen):
        """ - """
        screen.blit(self.image, self.rect)


class Decoration(pygame.sprite.Sprite):
    """ - """

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + (self.image.get_width() // 2), y + (self.image.get_height() // 2) + 5)
        # self.rect.midtop = (x * self.settings.tile_size // 2, y * (self.settings.tile_size - self.image.get_height()))
        # self.rect.midtop = (x, y)

    def draw(self, screen):
        """ - """
        screen.blit(self.image, self.rect)


if __name__ == '__main__':
    Game = Main()
    Game.main()
