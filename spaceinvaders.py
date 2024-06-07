import pygame
import math
import time
import random
from pygame import mixer

# Khởi tạo trò chơi
pygame.init()
timer = pygame.time.Clock()

# Tiêu đề và biểu tượng
pygame.display.set_caption('Bắn Ruồi')
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Tạo màn hình
screen = pygame.display.set_mode((1000, 600))

# Hình nền
background = pygame.image.load('background.jpg')

# Nhạc nền
mixer.music.load('background.wav')
mixer.music.play(-1)

class Player:
    """Lớp đại diện cho người chơi."""
    def __init__(self):
        """
        Khởi tạo đối tượng Player.

        Thuộc tính:
            image (Surface): Hình ảnh của người chơi.
            x, y (float): Tọa độ ban đầu của người chơi.
            change_x, change_y (float): Sự thay đổi tọa độ của người chơi.
        """
        self.image = pygame.image.load('player.png')
        self.x = 470
        self.y = 450
        self.change_x = 0
        self.change_y = 0

    def draw(self):
        """Vẽ người chơi lên màn hình."""
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        """Cập nhật vị trí của người chơi dựa trên sự thay đổi tọa độ."""
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

class Enemy:
    """Lớp đại diện cho kẻ địch."""
    def __init__(self):
        """
        Khởi tạo đối tượng Enemy.

        Thuộc tính:
            image (Surface): Hình ảnh của kẻ địch.
            x, y (float): Tọa độ ban đầu của kẻ địch.
            change_x, change_y (float): Sự thay đổi tọa độ của kẻ địch.
        """
        self.image = pygame.image.load('alien.png')
        self.x = random.randint(0, 936)
        self.y = random.randint(0, 220)
        self.change_x = 0.2
        self.change_y = 30

    def draw(self):
        """Vẽ kẻ địch lên màn hình."""
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        """Cập nhật vị trí của kẻ địch dựa trên sự thay đổi tọa độ."""
        self.x += self.change_x
        if self.x <= 0:
            self.change_x = 0.2
            self.y += self.change_y
        elif self.x >= 936:
            self.change_x = -0.2
            self.y += self.change_y

class Bullet:
    """Lớp đại diện cho viên đạn."""
    def __init__(self, x, y, owner, change_x, change_y):
        """
        Khởi tạo đối tượng Bullet.
        
        Tham số:
            x, y (float): Tọa độ ban đầu của viên đạn.
            owner (str): Chủ sở hữu viên đạn ('player' hoặc 'enemy').
            change_x, change_y (float): Sự thay đổi tọa độ của viên đạn.
        """
        self.image = pygame.image.load('goldbullet.png') if owner == 'player' else pygame.image.load('enemybullet.png')
        self.x = x
        self.y = y
        self.change_x = change_x
        self.change_y = change_y
        self.state = 'fire'
        self.owner = owner

    def move(self):
        """Cập nhật vị trí của viên đạn dựa trên sự thay đổi tọa độ."""
        self.x += self.change_x
        self.y += self.change_y
        if self.y <= 0 or self.y >= 600 or self.x <= 0 or self.x >= 1000:
            self.state = 'ready'

    def draw(self):
        """Vẽ viên đạn lên màn hình nếu nó đang ở trạng thái 'fire'."""
        if self.state == 'fire':
            screen.blit(self.image, (self.x, self.y))

class Boss:
    """Lớp đại diện cho trùm cuối."""
    def __init__(self):
        """
        Khởi tạo đối tượng Boss.

        Thuộc tính:
            image (Surface): Hình ảnh của trùm cuối.
            x, y (float): Tọa độ ban đầu của trùm cuối.
            change_x (float): Sự thay đổi tọa độ theo trục x của trùm cuối.
            health (int): Máu hiện tại của trùm cuối.
            max_health (int): Máu tối đa của trùm cuối.
        """
        self.image = pygame.image.load('boss.png')
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.x = 400
        self.y = 50
        self.change_x = 0.15
        self.health = 50
        self.max_health = 50

    def draw(self):
        """Vẽ trùm cuối lên màn hình và thanh máu của nó."""
        screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar()

    def move(self):
        """Cập nhật vị trí của trùm cuối dựa trên sự thay đổi tọa độ."""
        self.x += self.change_x
        if self.x <= 0 or self.x >= 872:
            self.change_x = -self.change_x

    def take_damage(self):
        """Giảm máu của trùm cuối."""
        self.health -= 1

    def draw_health_bar(self):
        """Vẽ thanh máu của trùm cuối."""
        health_bar_length = 128
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, health_bar_length, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, health_bar_length * health_ratio, 10))

    def fire_bullets(self, game):
        """
        Trùm cuối bắn đạn ngẫu nhiên theo các hướng khác nhau.
        
        Tham số:
            game (Game): Đối tượng Game để sử dụng phương thức fire_bullet.
        """
        number_of_bullets = random.randint(50, 60)
        for _ in range(number_of_bullets):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.2, 0.5)
            change_x = speed * math.cos(angle)
            change_y = speed * math.sin(angle)
            game.fire_bullet(self.x + 64, self.y + 64, 'enemy', change_x, change_y)

class Explosion:
    """Lớp đại diện cho vụ nổ."""
    def __init__(self, x, y):
        """
        Khởi tạo đối tượng Explosion.
        
        Tham số:
            x, y (float): Tọa độ của vụ nổ.
        """
        self.image = pygame.image.load('explosion.png')
        self.x = x
        self.y = y
        self.duration = 30

    def draw(self):
        """Vẽ vụ nổ lên màn hình nếu nó vẫn còn tồn tại."""
        if self.duration > 0:
            screen.blit(self.image, (self.x, self.y))
            self.duration -= 1

class Game:
    """Lớp đại diện cho trò chơi."""
    def __init__(self):
        """Khởi tạo đối tượng Game."""
        self.player = Player()
        self.enemies = [Enemy() for _ in range(random.randint(15, 20))]
        self.bullets = []
        self.explosions = []
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        self.win_font = pygame.font.Font('freesansbold.ttf', 64)
        self.enemy_fire_interval = 2000
        self.last_enemy_fire_time = pygame.time.get_ticks()
        self.game_over_flag = False
        self.boss = None
        self.last_player_fire_time = 0
        self.player_fire_delay = 250

    def fire_bullet(self, x, y, owner, change_x=0, change_y=-1):
        """
        Bắn một viên đạn.
        
        Tham số:
            x, y (float): Tọa độ của viên đạn.
            owner (str): Chủ sở hữu viên đạn ('player' hoặc 'enemy').
            change_x, change_y (float): Sự thay đổi tọa độ của viên đạn.
        """
        self.bullets.append(Bullet(x, y, owner, change_x, change_y))

    def is_collision(self, x1, y1, x2, y2, distance_threshold):
        """
        Kiểm tra va chạm giữa hai đối tượng dựa trên khoảng cách.

        Tham số:
            x1, y1, x2, y2 (float): Tọa độ của hai đối tượng.
            distance_threshold (float): Ngưỡng khoảng cách để xác định va chạm.
        
        Trả về:
            bool: True nếu có va chạm, ngược lại là False.
        """
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < distance_threshold

    def update_bullets(self):
        """Cập nhật và vẽ các viên đạn."""
        for bullet in self.bullets:
            bullet.move()
            bullet.draw()
            if bullet.state == 'ready':
                self.bullets.remove(bullet)
            else:
                if bullet.owner == 'player':
                    for enemy in self.enemies:
                        if self.is_collision(bullet.x, bullet.y, enemy.x + 27, enemy.y + 27, 27):
                            Explosive_Sound = mixer.Sound('punch.wav')
                            Explosive_Sound.play()
                            bullet.state = 'ready'
                            self.score += 10
                            self.enemies.remove(enemy)
                            self.explosions.append(Explosion(enemy.x, enemy.y))
                            break
                    if self.boss and self.is_collision(bullet.x, bullet.y, self.boss.x + 64, self.boss.y + 64, 64):
                        Explosive_Sound = mixer.Sound('punch.wav')
                        Explosive_Sound.play()
                        bullet.state = 'ready'
                        self.boss.take_damage()
                        self.explosions.append(Explosion(self.boss.x, self.boss.y))
                elif bullet.owner == 'enemy':
                    if self.is_collision(bullet.x, bullet.y, self.player.x + 16, self.player.y + 16, 27):
                        Explosive_Sound = mixer.Sound('endgame.mp3')
                        Explosive_Sound.play()
                        self.explosions.append(Explosion(self.player.x, self.player.y))
                        self.game_over_flag = True
                        return True
        return False

    def update_explosions(self):
        """Cập nhật và vẽ các vụ nổ."""
        for explosion in self.explosions:
            explosion.draw()
            if explosion.duration <= 0:
                self.explosions.remove(explosion)

    def show_score(self, x, y):
        """
        Hiển thị điểm số lên màn hình.

        Tham số:
            x, y (float): Tọa độ hiển thị điểm số.
        """
        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score_text, (x, y))

    def game_over(self):
        """Hiển thị thông báo kết thúc trò chơi và dừng nhạc nền."""
        game_over_text = self.game_over_font.render('GAME OVER', True, (255, 255, 255))
        screen.blit(game_over_text, (500 - game_over_text.get_width() // 2, 300 - game_over_text.get_height() // 2))
        mixer.music.stop()

    def you_won(self):
        """Hiển thị thông báo chiến thắng và dừng nhạc nền."""
        you_won_text = self.win_font.render('YOU WON', True, (255, 255, 255))
        screen.blit(you_won_text, (500 - you_won_text.get_width() // 2, 300 - you_won_text.get_height() // 2))
        mixer.music.stop()

    def run(self):
        """Chạy vòng lặp chính của trò chơi."""
        running = True
        while running:
            timer.tick(300)
            screen.fill((0, 255, 255))
            screen.blit(background, (0, 0))

            current_time = pygame.time.get_ticks()

            if current_time - self.last_enemy_fire_time > self.enemy_fire_interval:
                for enemy in self.enemies:
                    if random.random() < 0.3:
                        self.fire_bullet(enemy.x + 16, enemy.y + 10, 'enemy', 0, 0.5)
                if self.boss:
                    if random.random() < 0.5:
                        self.boss.fire_bullets(self)
                self.last_enemy_fire_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.change_x = -0.5
                    if event.key == pygame.K_RIGHT:
                        self.player.change_x = 0.5
                    if event.key == pygame.K_UP:
                        self.player.change_y = -0.5
                    if event.key == pygame.K_DOWN:
                        self.player.change_y = 0.5
                    if event.key == pygame.K_SPACE and len([b for b in self.bullets if b.owner == 'player']) < 3:
                        Bullet_Sound = mixer.Sound('laser.wav')
                        Bullet_Sound.play()
                        self.fire_bullet(self.player.x + 16, self.player.y, 'player', 0, -1)
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.player.change_x = 0
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.player.change_y = 0

            if not self.game_over_flag:
                self.player.move()
                self.player.draw()

                if self.boss:
                    self.boss.move()
                    self.boss.draw()
                    if self.is_collision(self.boss.x, self.boss.y, self.player.x, self.player.y, 64):
                        Explosive_Sound = mixer.Sound('endgame.mp3')
                        Explosive_Sound.play()
                        self.explosions.append(Explosion(self.player.x, self.player.y))
                        self.game_over_flag = True

                for enemy in self.enemies:
                    enemy.move()
                    enemy.draw()
                    if enemy.y > 400:
                        for e in self.enemies:
                            e.y = 2000
                        self.game_over_flag = True
                        break
                    if self.is_collision(enemy.x, enemy.y, self.player.x, self.player.y, 54):
                        Explosive_Sound = mixer.Sound('endgame.mp3')
                        Explosive_Sound.play()
                        self.explosions.append(Explosion(self.player.x, self.player.y))
                        self.game_over_flag = True
                        break

                if self.update_bullets():
                    self.game_over_flag = True

                self.update_explosions()

                if not self.enemies and not self.boss:
                    self.boss = Boss()

                if self.boss and self.boss.health <= 0:
                    self.score += 500
                    self.show_score(10,10)
                    self.you_won()
                    pygame.display.update()
                    time.sleep(2)
                    running = False

                self.show_score(10, 10)
            else:
                self.game_over()

            pygame.display.update()

if __name__=='__main__':
    game = Game()
    game.run()
    pygame.quit()