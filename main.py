import pygame
import random
import math
from pygame import mixer
import time

#inicializa o pygame
pygame.init()

#inicializa a tela
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

#define o título do jogo
pygame.display.set_caption('Space Invaders')

#define o ícone do jogo
icon = pygame.image.load('./assets/player/nave.png')
pygame.display.set_icon(icon)

#configurando os fundos
background = pygame.image.load('./assets/backgrounds/background.png')
stage_backgrounds = [
    pygame.image.load('./assets/backgrounds/stage1.png'),
    pygame.image.load('./assets/backgrounds/stage2.png'),
    pygame.image.load('./assets/backgrounds/stage3.png'),
    pygame.image.load('./assets/backgrounds/stage4.png'),
]
current_stage = 0

#música de fundo
mixer.music.load('./assets/sound/bg-music.wav')
mixer.music.play(-1)

#criando o jogador
playerImg = pygame.image.load('./assets/player/nave.png')
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 5
playerY_change = 0

#criando o inimigo
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./assets/enemies/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

#criando bala - estado pronto: bala não visível - estado de fogo: bala visível
bulletImg = pygame.image.load('./assets/elements/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

#imagem de explosão
burstImg = pygame.image.load('./assets/elements/burst.png')

#pontuação
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#texto de fim de jogo
go_font = pygame.font.Font('freesansbold.ttf', 64)

# Adicione essas novas variáveis após outras inicializações
GAME_FONT = pygame.font.Font('freesansbold.ttf', 32)
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 64)
start_button = pygame.Rect(300, 400, 200, 50)

# Sistema de vidas
player_lives = 3

# Variáveis para controle de fases
phase_start_time = 0
phase_duration = 10  # duração de cada fase em segundos

# Modifique a função draw_initial_screen
def draw_initial_screen():
    # Use a imagem de fundo inicial
    screen.blit(background, (0, 0))
    
    title = TITLE_FONT.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(title, (125, 200))
    
    pygame.draw.rect(screen, (0, 255, 255), start_button)
    start_text = GAME_FONT.render("Iniciar Jogo", True, (0, 0, 0))
    screen.blit(start_text, (310, 410))

def show_score(x, y):
    score = font.render("Pontuação: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    lives = font.render("Vidas: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives, (x, y + 40))

def game_over_text(x, y):
    go = go_font.render("FIM DE JOGO", True, (255, 255, 255))
    screen.blit(go, (200, 250))
    restart = font.render("Pressione R para Reiniciar ou Q para Sair", True, (255, 255, 255))
    screen.blit(restart, (200, 350))
    
def player(x, y):
    screen.blit(playerImg, (x, y))
    
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + playerImg.get_width() // 2 - bulletImg.get_width() // 2, y))
    
def burst(x, y):
    screen.blit(burstImg, (x, y))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def reset_game():
    global score_value, playerX, playerY, bulletX, bulletY, bullet_state, player_lives, phase_start_time, current_stage
    score_value = 0
    playerX = 370
    playerY = 480
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    player_lives = 3
    phase_start_time = time.time()
    current_stage = 0
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
    
running = True
game_started = False
game_over = False

while running:
    if not game_started:
        draw_initial_screen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    phase_start_time = time.time()
    else:
        #cor de fundo da tela
        screen.fill((0,0,0))
        #imagem de fundo
        screen.blit(stage_backgrounds[current_stage], (0, 0))
        
        # Verifica se é hora de mudar de fase
        current_time = time.time()
        if current_time - phase_start_time > phase_duration:
            current_stage = (current_stage + 1) % len(stage_backgrounds)
            phase_start_time = current_time
        
        for event in pygame.event.get(): #obtém um evento ocorrendo na tela (mouse ou teclado)
            if event.type == pygame.QUIT:
                running = False

            #verifica se uma tecla é pressionada, tecla esquerda ou direita
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    playerX_change = player_speed
                if event.key == pygame.K_UP:
                    playerY_change = -player_speed
                if event.key == pygame.K_DOWN:
                    playerY_change = player_speed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":  # Use '==' for comparison
                        #criando som de laser
                        laser = mixer.Sound('./assets/sound/laser.wav')
                        laser.play()
                        #obtendo a coordenada x da nave espacial
                        bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                        bulletY = playerY  # Start bullet from player's current Y position
                        fire_bullet(bulletX, bulletY)
                if game_over:
                    if event.key == pygame.K_r:
                        game_over = False
                        reset_game()
                    elif event.key == pygame.K_q:
                        running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0
            
        if not game_over:
            playerX += playerX_change
            playerY += playerY_change
            
            # jogador dentro do limite da janela
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736
            
            if playerY <= 0:
                playerY = 0
            elif playerY >= 536:  # Ajuste o valor conforme necessário para o limite inferior
                playerY = 536
            
            #movimento do inimigo
            for i in range(num_of_enemies):
                
                #fim de jogo
                if enemyY[i] > 440:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    game_over = True
                    break
                
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]
                    
                # Colisão da bala com o inimigo
                collision_bullet = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision_bullet and bullet_state == "fire":
                    # Criando som de colisão
                    burst(enemyX[i], enemyY[i])
                    explosion = mixer.Sound('./assets/sound/explosion.wav')
                    explosion.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)

                # Colisão do inimigo com a nave
                collision_player = isCollision(enemyX[i], enemyY[i], playerX, playerY)
                if collision_player:
                    burst(enemyX[i], enemyY[i])
                    explosion_sound = mixer.Sound('./assets/sound/explosion.wav')
                    explosion_sound.play()
                    player_lives -= 1
                    if player_lives <= 0:
                        for j in range(num_of_enemies):
                            enemyY[j] = 2000
                        game_over = True
                        break
                    else:
                        # Reset player position
                        playerX = 370
                        playerY = 480
                        # Reset enemy position
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i)
                
            #movimento da bala
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"
            
            if bullet_state == "fire":  # Use '==' for comparison
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change
            
            player(playerX, playerY)
            show_score(textX, textY)
        else:
            game_over_text(textX, textY)
        
        #atualizando o display
        pygame.display.update()
        clock.tick(60)  # limita FPS a 60
