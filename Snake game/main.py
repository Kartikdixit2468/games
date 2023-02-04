# Made by Kartik
from random import randint
import pygame


class MainWindow:
    """It contains settings of main window of screen"""

    def __init__(self, color):
        """Constructor of main game class"""
        pygame.init()
        self.color = color
        self.width = 1200
        self.height = 800
        self.screen = pygame.display
        self.main_screen = self.screen.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game by Kartik")
        self.main_screen.fill(self.color)
        pygame.display.update()
        self.score = 0
        self.snake_list = []
        self.snake_length = 0
        self.size = 30
        self.food_size = 20
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.velocity_x = 0
        self.velocity_y = 0
        self.snake_x_position = 45
        self.snake_y_position = 55
        self.food_x_position = randint(50, 700)
        self.food_y_position = randint(50, 700)
        self.game_over = False
        self.exit_game = False
        self.font = pygame.font.SysFont(None, 50)

    def blit_text(self, text, color, x_position, y_position):
        """This function will display text in screen"""
        scr_text = self.font.render(text, True, color)
        return self.main_screen.blit(scr_text, (x_position, y_position))

    @staticmethod
    def plot_snake_head(screen, color, head_list, size_):
        """This function plots the snake head on the main screen"""
        for x, y in head_list:
            pygame.draw.rect(screen, color, (x, y, size_, size_))

    def main(self):
        """Here the main game runs"""

        while not self.exit_game:
            if self.game_over:
                self.blit_text("Game Over", "black", 230, 200)
                self.blit_text("Press Enter to continue\n\n Press q to quit ", "black", 230, 240)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.exit_game = True

                        if event.key == pygame.K_RETURN:
                            self.game_over = False
                            self.velocity_x = 0
                            self.velocity_y = 0
                            self.snake_x_position = 45
                            self.snake_y_position = 55
                            self.snake_list = []
                            self.snake_length = 0
                            self.score = 0
                            self.main()

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if self.velocity_x == 6:
                                pass

                            else:
                                self.velocity_x -= 6
                                self.velocity_y = 0

                        if event.key == pygame.K_RIGHT:
                            if self.velocity_x == -6:
                                pass
                            else:
                                self.velocity_x += 6
                                self.velocity_y = 0

                        if event.key == pygame.K_DOWN:
                            if self.velocity_y == -6:
                                pass
                            else:
                                self.velocity_y += 6
                                self.velocity_x = 0

                        if event.key == pygame.K_UP:
                            if self.velocity_y == 6:
                                pass
                            else:
                                self.velocity_y -= 6
                                self.velocity_x = 0

            self.snake_x_position += self.velocity_x
            self.snake_y_position += self.velocity_y

            if abs(self.snake_x_position - self.food_x_position) < 20 and abs(self.snake_y_position - self.food_y_position) < 20:
                self.food_x_position = randint(100, 700)
                self.food_y_position = randint(50, 650)

                self.score = int(self.score) + 10
                self.snake_length += 5

            if self.snake_x_position > 1200:
                self.snake_x_position = 0

            if self.snake_x_position < 0:
                self.snake_x_position = 1200

            self.main_screen.fill(self.color)
            pygame.draw.rect(self.main_screen, "red", (self.food_x_position, self.food_y_position, self.food_size, self.food_size))

            snake_head = []
            snake_head.append(self.snake_x_position)
            snake_head.append(self.snake_y_position)
            self.snake_list.append(snake_head)

            self.plot_snake_head(self.main_screen, "blue", self.snake_list, self.size)
            pygame.draw.rect(self.main_screen, "pink", (self.snake_x_position, self.snake_y_position, self.size, self.size))

            if self.snake_y_position > 750 or self.snake_y_position < 20 or snake_head in self.snake_list[:-1]:
                self.velocity_y = 0
                self.velocity_x = 0
                self.game_over =true
            elif len(self.snake_list) > self.snake_length:
                del self.snake_list[0]

            pygame.draw.rect(self.main_screen, "black", [0, 0, 1210, 30])
            pygame.draw.rect(self.main_screen, "black", [0, 770, 1210, 30])

            text = f"Score: {self.score}"
            self.blit_text(text, 'black', 950, 35)
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    new_game = MainWindow("green")
    new_game.main()
