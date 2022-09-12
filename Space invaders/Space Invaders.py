import math
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.png')


# Hi-Scores
with open("Hi-Scores.txt", "r") as f:
    highScores = f.read()
# int(highScores)
print(highScores)
highScorefont = pygame.font.Font('freesansbold.ttf', 32)
highScoreX = 10
highScoreY = 75

# Sound
sound = True
bgmus = pygame.mixer.Sound("background.wav")
explosionSound = pygame.mixer.Sound("explosion.wav")
bulletSound = pygame.mixer.Sound("laser.wav")
gameovermus = pygame.mixer.Sound("gameover.wav")
bgmus.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = random.randint(1, 6)

def generate_enemy():
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change.append(40)

for i in range(num_of_enemies):
    generate_enemy()

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.7
bullet_state = "ready"

# Score

scoreNum = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(scoreNum), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def high_score(x, y):
    hiScore = font.render("Hi-Score: " + str(highScores), True, (255, 255, 255))
    screen.blit(hiScore, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Difficulty

gameLevel = 0
font = pygame.font.Font('freesansbold.ttf', 32)

levelX = 10
levelY = 40

def levelDifficulty(x, y):
    level = font.render("Difficulty : " + str(gameLevel), True, (255, 255, 255))
    screen.blit(level, (x, y))


gameover = False

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    if sound == True:
                        bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_m:
                volume = pygame.image.load("mute.png")
                screen.blit(volume, (32, 768))
                sound = False
                bgmus.stop()
            if event.key == pygame.K_p and sound == False:
                mute = pygame.image.load("sound.png")
                screen.blit(mute, (32, 768))
                sound = True
                bgmus.play(-1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            gameover = True
        
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            if sound == True:
                explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            scoreNum += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        scoreNum = int(scoreNum)
        if scoreNum >= 10 and scoreNum % 10 == 0:
            scoreNum += 1
            gameLevel += 1
            num_of_enemies += 1
            generate_enemy()
        # print(num_of_enemies)
        # print(enemySpeed)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Game over sound
    if gameover == True:
        if sound == True:
            bgmus.stop()
            gameovermus.play()
            gameovermus.stop()
        highScores = int(highScores)
        if scoreNum > highScores:
            with open("Hi-Scores.txt", "w") as f:
                scoreNum = str(scoreNum)
                f.write(scoreNum)

    player(playerX, playerY)
    show_score(textX, testY)
    levelDifficulty(levelX, levelY)
    high_score(highScoreX, highScoreY)
    pygame.display.update()

