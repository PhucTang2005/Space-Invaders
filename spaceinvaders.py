import pygame,random,math
from pygame import mixer

#Initialize the game
pygame.init()

#Title and icon

pygame.display.set_caption('Space Invaders')
icon=pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Create the screen
screen=pygame.display.set_mode((1000,600))   #the width and the height of the window (x,y)

# Background
background=pygame.image.load('background.jpg')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
PlayerImage=pygame.image.load('player.png')
PlayerX=470
PlayerY=450
Player_ChangeX=0
Player_ChangeY=0

def player(PlayerX,PlayerY):
    screen.blit(PlayerImage,(PlayerX,PlayerY))

# Enemy
EnemyImage=[]
EnemyX=[]
EnemyY=[]
Enemy_ChangeX=[]
Enemy_ChangeY=[]
num_of_enemies=random.randint(8,20)
for i in range(num_of_enemies):
    EnemyImage.append(pygame.image.load('alien.png'))
    EnemyX.append(random.randint(0,936))
    EnemyY.append(random.randint(0,220))
    Enemy_ChangeX.append(0.2)
    Enemy_ChangeY.append(30)

def enemy(EnemyX,EnemyY,i):
    screen.blit(EnemyImage[i],(EnemyX,EnemyY))

# Bullet
BulletImage=pygame.image.load('goldbullet.png')
BulletX=0
BulletY=450
Bullet_State='ready'
BulletX_Change=0
BulletY_Change=1

def fire_bullet(x,y):
    global Bullet_State
    Bullet_State='fire'
    screen.blit(BulletImage,(x+16,y+10))

# Create functions that checks collision
def Collision_Game_Over(EnemyX,EnemyY,PlayerX,PlayerY):
    distance=math.sqrt((EnemyX[i]-PlayerX)**2 + ((EnemyY[i]-PlayerY)**2))
    if distance < 54:
        return True
    else:
        return False
def Collision(EnemyX,EnemyY,BulletX,BulletY):
    distance=math.sqrt( (EnemyX-BulletX)**2 + ((EnemyY-BulletY)**2) )
    if distance < 27:
        return True
    else:
        return False
    
# Score 
total_score=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
def show_score(x,y):
    score=font.render('Score: ' + str(total_score), True, (255,255,255))
    screen.blit(score,(x,y))

# Game over
game_over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over():
    game_over=font.render('GAME OVER', True, (255,255,255))
    screen.blit(game_over,(400,300))

# Infinite loop to run game     
running=True
while running:
    # RGB: red, green, blue
    screen.fill((0,255,255))    #Cyan
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        # Check whether inputs from keyboard left or right or up or down
        if event.type==pygame.KEYDOWN:  # KEYDOWN: ấn vào 1 nút trên bàn phím
            if event.key==pygame.K_LEFT:
                Player_ChangeX=-0.2
            if event.key==pygame.K_RIGHT:
                Player_ChangeX=0.2
            if event.key==pygame.K_UP:
                Player_ChangeY-=0.2
            if event.key==pygame.K_DOWN:
                Player_ChangeY=0.2
            if event.key==pygame.K_SPACE:
                # Get the current coordinate of the spaceship
                if Bullet_State is 'ready':
                    Bullet_Sound=mixer.Sound('laser.wav')
                    Bullet_Sound.play()
                    BulletX=PlayerX
                    fire_bullet(BulletX,BulletY)

        if event.type==pygame.KEYUP:    # KEYUP: bỏ ngón tay ra khỏi phím đang ấn
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                Player_ChangeX=0
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                Player_ChangeY=0

    # Checking for boundaries

    # Player

    if PlayerX<=0:
        PlayerX=0
    if PlayerX>=936:
        PlayerX=936 
    if PlayerY<=0:
        PlayerY=0
    if PlayerY>=534:
        PlayerY=534

    player(PlayerX,PlayerY)
    PlayerX+=Player_ChangeX
    PlayerY+=Player_ChangeY

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if EnemyY[i]>400:
            for j in range(num_of_enemies):
                EnemyY[j]=2000
                game_over()
                break
            
        check_collision_Game_Over=Collision_Game_Over(EnemyX,EnemyY,PlayerX,PlayerY)
        
        if check_collision_Game_Over:
            Explosive_Sound=mixer.Sound('Bomman.wav')
            Explosive_Sound.play()
            game_over()
            break

        if EnemyX[i]<=0:
            Enemy_ChangeX[i]=0.2
            EnemyY[i]+=Enemy_ChangeY[i]
        if EnemyX[i]>=936:
            Enemy_ChangeX[i]=-0.2
            EnemyY[i]+=Enemy_ChangeY[i]

        # Check collision
        check_collision=Collision(EnemyX[i],EnemyY[i],BulletX,BulletY)
        if check_collision:
            Explosive_Sound=mixer.Sound('punch.wav')
            Explosive_Sound.play()
            BulletY=450
            Bullet_State='ready'
            total_score+=10
            EnemyX[i]=random.randint(0,936)
            EnemyY[i]=random.randint(0,220)
        enemy(EnemyX[i],EnemyY[i],i)
        EnemyX[i]+=Enemy_ChangeX[i]
            

    #Bullet 
    if BulletY<=0:
        BulletY=450
        Bullet_State='ready'
    if Bullet_State is 'fire':
        fire_bullet(BulletX,BulletY)
        BulletY-=BulletY_Change
    show_score(textX,textY)
    pygame.display.update() # Update continously