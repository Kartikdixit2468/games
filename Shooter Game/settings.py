# Made by kartik


class Settings:
    """Contain the settings of our game"""
    def __init__(self):
        """Initializes the game setting objects"""

        # Display
        self.screen_width = 1200
        self.screen_height = 800

        # Main Game
        self.fps = 60
        self.bg_color = (144, 201, 120)
        self.jump_speed = 0
        self.gravity = 2.2 * 2
        # self.gravity = 0
        self.tile_size = 20

        # Player
        self.p_scale = 1.6
        self.p_x = 50
        self.p_y = 422
        self.p_speed = 7 * 2
        self.p_y_speed = 0
        self.p_ammo = 12
        self.p_grenades = 10

        # Enemy
        self.enemy_scale = 1.6
        self.enemy_x = 700
        self.enemy_y = 422
        self.enemy_speed = 6 * 2
        self.e_ammo = 5000
        self.e_grenades = 0
        self.enemy_jump_speed = 0

        # Bullet
        self.bullet_speed = 20 * 2
        self.shoot_cooldown = 0
        self.shoot_cooldown_b = 8

        # Soldier
        self.health = 100
        self.max_health = 100

        # Grenade
        self.grenade_speed = 16 * 1.6
        self.grenade_y_speed = -25 * 1.6

        # Explosion
        self.explosion_speed = 3

        # Map
        self.tile_types = 21
        self.rows = 16
        self.columns = 150
        self.y_additional_space = 22


if __name__ == '__main__':
    pass
