import pygame.draw

from settings import Settings


class HealthBar:
    """ Creates and draws a health bar on the game screen """
    def __init__(self, x, y, health, max_health):
        """
        Constructor of the class
        Initializes the game objects
        :param x:  Represents the x coordinate of Health bar
        :param y:  Represents the Y coordinate of Health bar
        :param health:  Represents the health of the player
        :param max_health:  Represents the maximum health of the player

        """
        self.settings = Settings()
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw_health_bar(self, screen, health):
        """ This draws the rectangle which represents the health """
        self.health = health
        if self.health == 0:
            ratio = 0
        elif self.health >= self.max_health:
            ratio = 1
        else:
            ratio = self.health / self.max_health
        pygame.draw.rect(screen, 'black', (self.x - 2, self.y - 2, 150 + 5, 20 + 5))
        pygame.draw.rect(screen, 'red', (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, 'green', (self.x, self.y, 150 * ratio, 20))


if __name__ == '__main__':
    pass
