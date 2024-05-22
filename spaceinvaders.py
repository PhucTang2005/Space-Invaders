import pygame, random, math
from pygame import mixer

# Initialize the game
pygame.init()

# Title and icon
pygame.display.set_caption('Bắn Ruồi')
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Create the screen
screen = pygame.display.set_mode((1000, 600))   # the width and the height of the window (x,y)

# Background
background = pygame.image.load('background.jpg')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player class
class Player:
    def __init__(self):
        self.image = pygame.image.load('player.png')
        self.x = 470
        self.y = 450
        self.change_x = 0
        self.change_y = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.change_x
        self.y += self.change_y
        if self.x <= 0:
            self.x = 0
        if self.x >= 936:
            self.x = 936 
        if self.y <= 0:
            self.y = 0
        if self.y >= 534:
            self.y = 534

# Enemy class
class Enemy:
    def __init__(self):
        self.image = pygame.image.load('alien.png')
        self.x = random.randint(0, 936)
        self.y = random.randint(0, 220)
        self.change_x = 0.2
        self.change_y = 30

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.change_x
        if self.x <= 0:
            self.change_x = 0.2
            self.y += self.change_y
        elif self.x >= 936:
            self.change_x = -0.2
            self.y += self.change_y

# Bullet class
class Bullet:
    def __init__(self):
        self.image = pygame.image.load('goldbullet.png')
        self.x = 0
        self.y = 450
        self.change_x = 0
        self.change_y = 1
        self.state = 'ready'

    def fire(self, x, y):
        self.state = 'fire'
        screen.blit(self.image, (x + 16, y + 10))

    def move(self):
        if self.state == 'fire':
            self.fire(self.x, self.y)
            self.y -= self.change_y
        if self.y <= 0:
            self.y = 450
            self.state = 'ready'

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(random.randint(8, 20))]
        self.bullet = Bullet()
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(self, x, y):
        score = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over(self):
        game_over_text = self.game_over_font.render('GAME OVER', True, (255, 255, 255))
        screen.blit(game_over_text, (400, 300))

    def is_collision(self, x1, y1, x2, y2, distance_threshold):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance < distance_threshold

    def run(self):
        running = True
        while running:
            screen.fill((0, 255, 255))    # Cyan
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.change_x = -0.2
                    if event.key == pygame.K_RIGHT:
                        self.player.change_x = 0.2
                    if event.key == pygame.K_UP:
                        self.player.change_y -= 0.2
                    if event.key == pygame.K_DOWN:
                        self.player.change_y = 0.2
                    if event.key == pygame.K_SPACE and self.bullet.state == 'ready':
                        Bullet_Sound = mixer.Sound('laser.wav')
                        Bullet_Sound.play()
                        self.bullet.x = self.player.x
                        self.bullet.state = 'fire'
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.player.change_x = 0
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.player.change_y = 0

            self.player.move()
            self.player.draw()

            for enemy in self.enemies:
                enemy.move()
                enemy.draw()

                if enemy.y > 400:
                    for e in self.enemies:
                        e.y = 2000
                    self.game_over()
                    break

                if self.is_collision(enemy.x, enemy.y, self.player.x, self.player.y, 54):
                    Explosive_Sound = mixer.Sound('endgame.mp3')
                    Explosive_Sound.play()
                    self.game_over()
                    running = False
                    break

                if self.is_collision(enemy.x, enemy.y, self.bullet.x, self.bullet.y, 27):
                    Explosive_Sound = mixer.Sound('punch.wav')
                    Explosive_Sound.play()
                    self.bullet.y = 450
                    self.bullet.state = 'ready'
                    self.score += 10
                    enemy.x = random.randint(0, 936)
                    enemy.y = random.randint(0, 220)

            self.bullet.move()
            self.show_score(10, 10)
            pygame.display.update()

# Main loop
if __name__ == "__main__":
    game = Game()
    game.run()
