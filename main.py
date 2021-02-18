import pygame
import random
from pygame import mixer

# Initilize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Adding Background
background = pygame.image.load("space2.jpg")


#Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)



# Title and Icon
pygame.display.set_caption("Infinite Space")
icon = pygame.image.load("del.jpg")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))  # Draw image on screen


#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX = 10
textY =10

#Game Over text
over_font = pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    score = font.render("Score:  "+ str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))


def game_over_text():
    over_text = over_font.render("Your world is occupied"+ str(score_value), True, (255,255,255))
    screen.blit(over_text, (200, 250))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load("enemy2.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)



# Bullet
# Ready - You cant see the bullet on the scree n
# Fire The Bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.3
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX,enemY,bulletX,bulletY):
    distance = ((enemyX-bulletX)**2 + (enemY-bulletY)**2)**0.5
    #distance math.sqrt((math.pow(enemyX-bullextX,2)) + (math.pow(enemY-bulletY,2)))
    if distance <27:
        return True
    else:
        return False

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Create variable called running because of broke loop when we want a time
running = True
while running:
    # RGB  - Red,  Green,  Blue Hemen hemen her şeyin üzerinde olmalı ki resimler görünsün eğer resimlerden sonra yapılırsa ekran sadece renk olarak görünür
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))
    # Second Loop's aim is keep everything done and traverse on the all of event
    for event in pygame.event.get():
        # If we press X button broke while loop and we can exit from game.
        if event.type == pygame.QUIT:
            running = False

        # tuş vuruşuna basılırsa sağını veya solunu kontrol edin(if keystroke is pressed check its right or left )
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Sol tuşa basıldıysa
                playerX_change = -0.1

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1

            if event.key == pygame.K_UP:
                playerY_change = -0.1

            if event.key == pygame.K_DOWN:
                playerY_change = 0.1

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Checking Boundries

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 736 çünkü 64 piksel uzay aracının pikseli  PNG boyutunu 64x64 seçmiştim 800-64 = 736
        playerX = 736

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    player(playerX, playerY)

    # Enemy Movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over_text()
                break



        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 736 çünkü 64 piksel uzay aracının pikseli  PNG boyutunu 64x64 seçmiştim 800-64 = 736
            enemyX_change[i] = -0.1
            enemyY[i] += enemyY_change[i]
            # Eğer X ekseninde simterik bir şekilde geri dönmesini istiyorsun enemyX = -0.1
            # Eğer X eksenine çarpıp dönsün istiyorsa enemyX_change = -0.1

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)


    #Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    show_score(textX,textY)
    #   enemyY += enemyY_change
    # if enemyY <= 0:
    # enemyY_change = 0.1
    # elif enemyY >= 536:
    # enemyY_change = -0.1
    # Eğer 5 yorum satırını kaldırırsan Y ekseninde de hareket eden bir enemy gorursun


    pygame.display.update()  # Bunu yapmamızın nedeni renk verilse bile update edilmeden çalışmayacak olması
    # update mermi atıldığında skor alındıgında kısaca her değişiklikte ekranı oyunu güncellemelidir bu yüzden 2. sırada calısır ınıtten sonra



    #1:30:10