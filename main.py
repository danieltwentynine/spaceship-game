import pygame
import random
import math
import asyncio
from pygame import mixer

# Initialize Pygame
pygame.init()

# Initialize game display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Set the game title
pygame.display.set_caption('Space Invaders')

# Set game title icon
icon = pygame.image.load('airship.png')
pygame.display.set_icon(icon)

# Setting background
background = pygame.image.load('background.png')

# Background music
mixer.music.load('bg-music.wav')
mixer.music.play(-1)

# Creating player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 5

# Creating enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Creating bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Burst image - explosion
burstImg = pygame.image.load('burst.png')

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
go_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    go = go_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def burst(x, y):
    screen.blit(burstImg, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

async def main():
    global playerX, playerX_change, bulletY, bullet_state, score_value

    running = True
    while running:
        # Screen background color
        screen.fill((0, 0, 0))
        # Background image
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check if key is pressed, left key or right key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    playerX_change = player_speed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        # Creating laser sound
                        laser = mixer.Sound('laser.wav')
                        laser.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        
        # Player inside window boundary
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement
        for i in range(num_of_enemies):
            # Game over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text(textX, textY)
                break
            
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]
                
            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                burst(enemyX[i], enemyY[i])
                explosion = mixer.Sound('explosion.wav')
                explosion.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            
            enemy(enemyX[i], enemyY[i], i)
            
        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            
        player(playerX, playerY)
        show_score(textX, textY)
        
        # Updating display
        pygame.display.update()
        await asyncio.sleep(0)  # Allow other tasks to run
        clock.tick(60)  # Limits FPS to 60

# Run the main function
asyncio.run(main())