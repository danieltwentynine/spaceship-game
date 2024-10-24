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
playerImg = pygame.transform.scale(playerImg, (80, 80))
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

# Load explosion images for animation
burst_images = []
for i in range(1, 6):  # Assuming we have 5 explosion images
    burst_images.append(pygame.image.load(f'./assets/elements/explosion-{i}.png'))
burst_index = 0
burst_timer = 0
BURST_FRAME_DURATION = 3  # Reduced duration for more fluid animation

# Function to handle explosion animation
def burst(x, y, alpha):
    global burst_index, burst_timer
    if burst_index < len(burst_images):
        image = burst_images[burst_index].copy()
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
        burst_timer += 1
        if burst_timer >= BURST_FRAME_DURATION:
            burst_index += 1
            burst_timer = 0
    else:
        burst_index = 0  # Reset the animation

#pontuação
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#texto de fim de jogo
go_font = pygame.font.Font('freesansbold.ttf', 64)

# Adicione essas novas variáveis após outras inicializações
GAME_FONT = pygame.font.Font('freesansbold.ttf', 20)
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
start_button = pygame.Rect(300, 400, 200, 50)

# Sistema de vidas
player_lives = 3

# Variáveis para controle de fases
phase_start_time = 0
phase_duration = 10  # duração de cada fase em segundos

# Add variables for player blinking
player_blinking = False
player_blink_start = 0
player_blink_duration = 2000  # 2 seconds of blinking
player_blink_interval = 200  # Blink every 200 ms

# Modifique a função draw_initial_screen
def draw_initial_screen():
    # Use a imagem de fundo inicial
    screen.blit(background, (0, 0))
    
    title = TITLE_FONT.render("SPACE INVADERS", True, (255, 255, 255))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(title, title_rect)
    
    pygame.draw.rect(screen, (0, 255, 255), start_button)
    start_text = GAME_FONT.render("Iniciar Jogo", True, (0, 0, 0))
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

def show_score(x, y):
    score = font.render("Pontuação: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    lives = font.render("Vidas: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives, (x, y + 40))

def game_over_text():
    go = go_font.render("FIM DE JOGO", True, (255, 255, 255))
    go_rect = go.get_rect(center=(screen.get_width() // 2, 250))
    screen.blit(go, go_rect)
    restart = font.render("Pressione R para Reiniciar ou Q para Sair", True, (255, 255, 255))
    restart_rect = restart.get_rect(center=(screen.get_width() // 2, 350))
    screen.blit(restart, restart_rect)
def player(x, y):
    screen.blit(playerImg, (x, y))
    
def enemy(x, y, i, alpha=255):
    enemy_surface = enemyImg[i].copy()
    enemy_surface.set_alpha(alpha)
    screen.blit(enemy_surface, (x, y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + playerImg.get_width() // 2 - bulletImg.get_width() // 2, y))
    
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
    
# Add a new variable for interpolation speed
interpolation_speed = 0.1  # Adjust this value to change the delay effect

running = True
game_started = False
game_over = False

# New variables for explosion animation
exploding_enemies = {}
EXPLOSION_DURATION = 30  # Duration of explosion animation in frames

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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        laser = mixer.Sound('./assets/sound/laser.wav')
                        laser.play()
                        bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                        bulletY = playerY
                        fire_bullet(bulletX, bulletY)
                if game_over:
                    if event.key == pygame.K_r:
                        game_over = False
                        reset_game()
                    elif event.key == pygame.K_q:
                        running = False

        if not game_over:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()
            
            # Interpolate player position towards mouse position
            playerX += (mouseX - playerX - playerImg.get_width() // 2) * interpolation_speed
            playerY += (mouseY - playerY - playerImg.get_height() // 2) * interpolation_speed
            
            # jogador dentro do limite da janela
            playerX = max(0, min(playerX, 736))
            playerY = max(0, min(playerY, 536))
            
            #movimento do inimigo
            for i in range(num_of_enemies):
                if i in exploding_enemies:
                    # Continue explosion animation
                    exploding_enemies[i]['timer'] += 1
                    alpha = int(255 * (1 - exploding_enemies[i]['timer'] / EXPLOSION_DURATION))
                    burst(enemyX[i], enemyY[i], alpha)
                    enemy(enemyX[i], enemyY[i], i, alpha)
                    
                    if exploding_enemies[i]['timer'] >= EXPLOSION_DURATION:
                        # Reset enemy position after explosion
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)
                        del exploding_enemies[i]
                    continue
                
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
                    explosion = mixer.Sound('./assets/sound/explosion.wav')
                    explosion.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    
                    # Start explosion animation
                    exploding_enemies[i] = {'timer': 0}

                # Colisão do inimigo com a nave
                collision_player = isCollision(enemyX[i], enemyY[i], playerX, playerY)
                if collision_player:
                    explosion_sound = mixer.Sound('./assets/sound/explosion.wav')
                    explosion_sound.play()
                    player_lives -= 1
                    if player_lives <= 0:
                        for j in range(num_of_enemies):
                            enemyY[j] = 2000
                        game_over = True
                        break
                    else:
                        # Start blinking effect
                        player_blinking = True
                        player_blink_start = pygame.time.get_ticks()
                        # Reset enemy position
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i)
                
            #movimento da bala
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"
            
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change
            
            # Handle player blinking
            if player_blinking:
                current_time = pygame.time.get_ticks()
                if current_time - player_blink_start < player_blink_duration:
                    # Toggle visibility based on blink interval
                    if (current_time // player_blink_interval) % 2 == 0:
                        player(playerX, playerY)
                else:
                    player_blinking = False
            else:
                player(playerX, playerY)
            
            show_score(textX, textY)
        else:
            game_over_text()
        
        #atualizando o display
        pygame.display.update()
        clock.tick(60)  # limita FPS a 60
