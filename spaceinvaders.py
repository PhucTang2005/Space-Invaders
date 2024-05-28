import pygame, math, time, random
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
    """
    Lớp đại diện cho người chơi.

    Thuộc tính:
        image (pygame.Surface): Hình ảnh của người chơi.
        x (float): Tọa độ x của người chơi.
        y (float): Tọa độ y của người chơi.
        change_x (float): Thay đổi tọa độ x để di chuyển người chơi.
        change_y (float): Thay đổi tọa độ y để di chuyển người chơi.
    """
    def __init__(self):
        """Khởi tạo người chơi với hình ảnh, vị trí và tốc độ di chuyển."""
        self.image = pygame.image.load('player.png')
        self.x = 470
        self.y = 450
        self.change_x = 0
        self.change_y = 0

    def draw(self):
        """Vẽ người chơi lên màn hình."""
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        """Cập nhật vị trí của người chơi dựa trên thay đổi tọa độ."""
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
    """
    Lớp đại diện cho kẻ địch.

    Thuộc tính:
        image (pygame.Surface): Hình ảnh của kẻ địch.
        x (float): Tọa độ x của kẻ địch.
        y (float): Tọa độ y của kẻ địch.
        change_x (float): Thay đổi tọa độ x để di chuyển kẻ địch.
        change_y (float): Thay đổi tọa độ y để di chuyển kẻ địch.
    """
    def __init__(self):
        """Khởi tạo kẻ địch với hình ảnh, vị trí ngẫu nhiên và tốc độ di chuyển."""
        self.image = pygame.image.load('alien.png')
        self.x = random.randint(0, 936)
        self.y = random.randint(0, 220)
        self.change_x = 0.2
        self.change_y = 30

    def draw(self):
        """Vẽ kẻ địch lên màn hình."""
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        """Cập nhật vị trí của kẻ địch dựa trên thay đổi tọa độ."""
        self.x += self.change_x
        if self.x <= 0:
            self.change_x = 0.2
            self.y += self.change_y
        elif self.x >= 936:
            self.change_x = -0.2
            self.y += self.change_y

class Bullet:
    """
    Lớp đại diện cho đạn.

    Thuộc tính:
        image (pygame.Surface): Hình ảnh của đạn.
        x (float): Tọa độ x của đạn.
        y (float): Tọa độ y của đạn.
        change_y (float): Thay đổi tọa độ y để di chuyển đạn.
        state (str): Trạng thái của đạn ('fire' hoặc 'ready').
        owner (str): Chủ sở hữu đạn ('player' hoặc 'enemy').
    """
    def __init__(self, x, y, owner):
        """Khởi tạo đạn với hình ảnh, vị trí và chủ sở hữu."""
        self.image = pygame.image.load('goldbullet.png') if owner == 'player' else pygame.image.load('enemybullet.png')
        self.x = x
        self.y = y
        self.change_y = 1 if owner == 'player' else -1
        self.state = 'fire'
        self.owner = owner

    def move(self):
        """Cập nhật vị trí của đạn dựa trên thay đổi tọa độ."""
        self.y -= self.change_y
        if self.y <= 0 or self.y >= 600:
            self.state = 'ready'

    def draw(self):
        """Vẽ đạn lên màn hình."""
        screen.blit(self.image, (self.x, self.y))

class Explosion:
    """
    Lớp đại diện cho hiệu ứng nổ.

    Thuộc tính:
        image (pygame.Surface): Hình ảnh của hiệu ứng nổ.
        x (float): Tọa độ x của hiệu ứng nổ.
        y (float): Tọa độ y của hiệu ứng nổ.
        duration (int): Thời gian hiển thị hiệu ứng nổ (tính theo frame).
    """
    def __init__(self, x, y):
        """Khởi tạo hiệu ứng nổ với hình ảnh và vị trí."""
        self.image = pygame.image.load('explosion.png')
        self.x = x
        self.y = y
        self.duration = 30

    def draw(self):
        """Vẽ hiệu ứng nổ lên màn hình và giảm thời gian hiển thị."""
        if self.duration > 0:
            screen.blit(self.image, (self.x, self.y))
            self.duration -= 1

class Game:
    """
    Lớp đại diện cho trò chơi.

    Thuộc tính:
        player (Player): Người chơi.
        enemies (list): Danh sách các kẻ địch.
        bullets (list): Danh sách các viên đạn.
        explosions (list): Danh sách các hiệu ứng nổ.
        score (int): Điểm số của người chơi.
        font (pygame.font.Font): Font chữ để hiển thị điểm số.
        game_over_font (pygame.font.Font): Font chữ để hiển thị thông báo kết thúc trò chơi.
        win_font (pygame.font.Font): Font chữ để hiển thị thông báo chiến thắng.
        enemy_fire_interval (int): Khoảng thời gian giữa các lần kẻ địch bắn đạn.
        last_enemy_fire_time (int): Thời điểm lần cuối cùng kẻ địch bắn đạn.
        game_over_flag (bool): Cờ để kiểm tra trạng thái kết thúc trò chơi.
    """
    def __init__(self):
        """Khởi tạo trò chơi với người chơi, kẻ địch, đạn, hiệu ứng nổ, điểm số và các thiết lập khác."""
        self.player = Player()
        self.enemies = [Enemy() for _ in range(random.randint(10, 15))]
        self.bullets = []
        self.explosions = []
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        self.win_font = pygame.font.Font('freesansbold.ttf', 64)
        self.enemy_fire_interval = 2000
        self.last_enemy_fire_time = pygame.time.get_ticks()
        self.game_over_flag = False

    def show_score(self, x, y):
        """Hiển thị điểm số lên màn hình."""
        score = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        screen.blit(score, (x, y))

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

    def is_collision(self, x1, y1, x2, y2, distance_threshold):
        """
        Kiểm tra va chạm giữa hai đối tượng dựa trên khoảng cách.

        Tham số:
            x1, y1 (float): Tọa độ của đối tượng thứ nhất.
            x2, y2 (float): Tọa độ của đối tượng thứ hai.
            distance_threshold (float): Khoảng cách để xác định va chạm.

        Trả về:
            bool: True nếu có va chạm, ngược lại False.
        """
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance < distance_threshold

    def fire_bullet(self, x, y, owner):
        """Bắn đạn từ vị trí xác định và thêm vào danh sách đạn."""
        bullet = Bullet(x, y, owner)
        self.bullets.append(bullet)

    def update_bullets(self):
        """
        Cập nhật và vẽ các viên đạn.

        Trả về:
            bool: True nếu trò chơi kết thúc, ngược lại False.
        """
        for bullet in self.bullets:
            bullet.move()
            bullet.draw()
            if bullet.state == 'ready':
                self.bullets.remove(bullet)
            else:
                if bullet.owner == 'player':
                    for enemy in self.enemies:
                        if self.is_collision(enemy.x, enemy.y, bullet.x, bullet.y, 27):
                            Explosive_Sound = mixer.Sound('punch.wav')
                            Explosive_Sound.play()
                            bullet.state = 'ready'
                            self.score += 10
                            self.enemies.remove(enemy)
                            self.explosions.append(Explosion(enemy.x, enemy.y))
                            break
                elif bullet.owner == 'enemy':
                    if self.is_collision(self.player.x, self.player.y, bullet.x, bullet.y, 27):
                        Explosive_Sound = mixer.Sound('endgame.mp3')
                        Explosive_Sound.play()
                        self.explosions.append(Explosion(self.player.x, self.player.y))
                        self.game_over_flag = True
                        return True
        return False

    def update_explosions(self):
        """Cập nhật và vẽ các hiệu ứng nổ."""
        for explosion in self.explosions:
            explosion.draw()
        self.explosions = [explosion for explosion in self.explosions if explosion.duration > 0]

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
                        self.fire_bullet(enemy.x + 16, enemy.y + 10, 'enemy')
                self.last_enemy_fire_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.change_x = -0.2
                    if event.key == pygame.K_RIGHT:
                        self.player.change_x = 0.2
                    if event.key == pygame.K_UP:
                        self.player.change_y = -0.2
                    if event.key == pygame.K_DOWN:
                        self.player.change_y = 0.2
                    if event.key == pygame.K_SPACE and len([b for b in self.bullets if b.owner == 'player']) < 3:
                        Bullet_Sound = mixer.Sound('laser.wav')
                        Bullet_Sound.play()
                        self.fire_bullet(self.player.x + 16, self.player.y, 'player')
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.player.change_x = 0
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.player.change_y = 0

            if not self.game_over_flag:
                self.player.move()
                self.player.draw()

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

                if not self.enemies:
                    self.you_won()
                    pygame.display.update()
                    time.sleep(2)
                    running = False

                self.show_score(10, 10)
            else:
                self.game_over()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
