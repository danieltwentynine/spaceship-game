# Importa o módulo pygame para criar o jogo
import pygame
# Importa o módulo random para gerar números aleatórios
import random
# Importa o módulo math para cálculos matemáticos
import math
# Importa o módulo mixer do pygame para trabalhar com sons
from pygame import mixer
# Importa o módulo time para controle de tempo
import time

# Inicializa todos os módulos do pygame
pygame.init()

# Cria a janela do jogo com dimensões 800x600 pixels
screen = pygame.display.set_mode((800, 600))
# Cria um objeto para controlar o FPS do jogo
clock = pygame.time.Clock()

# Define o título da janela do jogo
pygame.display.set_caption('Space Invaders')

# Carrega e define o ícone da janela do jogo
icon = pygame.image.load('./assets/player/nave.png')
pygame.display.set_icon(icon)

# Carrega a imagem de fundo principal
background = pygame.image.load('./assets/backgrounds/background.png')
# Carrega as imagens de fundo para cada fase do jogo
stage_backgrounds = [
    pygame.image.load('./assets/backgrounds/stage1.png'),
    pygame.image.load('./assets/backgrounds/stage2.png'),
    pygame.image.load('./assets/backgrounds/stage3.png'),
    pygame.image.load('./assets/backgrounds/stage4.png'),
]
# Define a fase atual como 0 (primeira fase)
current_stage = 0

# Carrega e inicia a música de fundo em loop infinito
# mixer.music.load('./assets/sound/bg-music.wav')
# mixer.music.play(-1)

# Carrega e configura a imagem do jogador
playerImg = pygame.image.load('./assets/player/nave.png')
playerImg = pygame.transform.scale(playerImg, (80, 80))
# Define a posição inicial do jogador
playerX = 370
playerY = 480
# Define as variáveis de movimento do jogador
playerX_change = 0
player_speed = 5
playerY_change = 0

# Cria listas vazias para armazenar múltiplos inimigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
# Define o número total de inimigos
num_of_enemies = 6

# Inicializa cada inimigo com posições e velocidades aleatórias
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./assets/enemies/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Carrega a imagem da bala e configura suas variáveis
bulletImg = pygame.image.load('./assets/elements/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Carrega as imagens da explosão para animação
burst_images = []
# Carrega 5 imagens de explosão diferentes
for i in range(1, 6):
    burst_images.append(pygame.image.load(f'./assets/elements/explosion-{i}.png'))
burst_index = 0
burst_timer = 0
BURST_FRAME_DURATION = 3  # Duração de cada frame da explosão

# Função para animar a explosão
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
        burst_index = 0  # Reinicia a animação

# Inicializa o sistema de pontuação
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Define a posição do texto da pontuação
textX = 10
textY = 10

# Define a fonte para o texto de fim de jogo
go_font = pygame.font.Font('freesansbold.ttf', 64)

# Define fontes para diferentes textos do jogo
GAME_FONT = pygame.font.Font('freesansbold.ttf', 20)
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
# Cria um retângulo para o botão de início
start_button = pygame.Rect(300, 400, 200, 50)

# Inicializa o sistema de vidas do jogador
player_lives = 3

# Variáveis para o efeito de piscar do jogador
player_blinking = False
player_blink_start = 0
player_blink_duration = 2000  # 2 segundos de piscar
player_blink_interval = 200  # Pisca a cada 200ms

# Variável para contar inimigos destruídos
enemies_destroyed = 0
# Variáveis para controle de transição de fase
transitioning = False
transition_alpha = 0
transition_direction = 1  # 1 para fade in, -1 para fade out
transition_delay = 1000  # 1 segundo de delay
transition_start_time = 0
transition_speed = 3  # Velocidade do fade

# Adicione estas variáveis globais no início do arquivo, junto com as outras
transition_surface = pygame.Surface((800, 600))
transition_surface.fill((0, 0, 0))
waiting_for_next_stage = False

# Função para desenhar a transição de fase
def draw_transition():
    global transition_alpha, transitioning, transition_direction, transition_start_time, game_started, waiting_for_next_stage, enemies_destroyed
    
    if transitioning:
        current_time = pygame.time.get_ticks()
        
        # Fade out (escurecer)
        if transition_direction == 1:
            transition_alpha = min(255, transition_alpha + transition_speed)
            transition_surface.set_alpha(transition_alpha)
            screen.blit(transition_surface, (0, 0))
            
            # Quando completar o fade out
            if transition_alpha >= 255:
                # Reseta posições dos inimigos
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)
                
                # Mostra texto da próxima fase
                stage_text = TITLE_FONT.render(f"Fase {current_stage + 1}", True, (255, 255, 255))
                stage_text_rect = stage_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                screen.blit(stage_text, stage_text_rect)
                
                # Aguarda input do jogador
                press_text = GAME_FONT.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
                press_rect = press_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
                screen.blit(press_text, press_rect)
                
                waiting_for_next_stage = True
                transition_direction = -1
        
        # Fade in (clarear)
        elif transition_direction == -1 and not waiting_for_next_stage:
            transition_alpha = max(0, transition_alpha - transition_speed)
            transition_surface.set_alpha(transition_alpha)
            screen.blit(transition_surface, (0, 0))
            
            # Quando completar o fade in
            if transition_alpha <= 0:
                transitioning = False
                enemies_destroyed = 0

# Função para desenhar a tela inicial
def draw_initial_screen():
    # Desenha o fundo
    screen.blit(background, (0, 0))
    
    # Desenha o título
    title = TITLE_FONT.render("SPACE INVADERS", True, (255, 255, 255))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(title, title_rect)
    
    # Desenha o botão de início
    pygame.draw.rect(screen, (0, 255, 255), start_button)
    start_text = GAME_FONT.render("Iniciar Jogo", True, (0, 0, 0))
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

# Função para mostrar a pontuação e vidas
def show_score(x, y):
    score = font.render("Pontuação: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    lives = font.render("Vidas: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives, (x, y + 40))

# Função para mostrar texto de fim de jogo
def game_over_text():
    go = go_font.render("FIM DE JOGO", True, (255, 255, 255))
    go_rect = go.get_rect(center=(screen.get_width() // 2, 250))
    screen.blit(go, go_rect)
    restart = font.render("Pressione R para Reiniciar ou Q para Sair", True, (255, 255, 255))
    restart_rect = restart.get_rect(center=(screen.get_width() // 2, 350))
    screen.blit(restart, restart_rect)

# Função para desenhar o jogador
def player(x, y):
    screen.blit(playerImg, (x, y))
    
# Função para desenhar o inimigo
def enemy(x, y, i, alpha=255):
    enemy_surface = enemyImg[i].copy()
    enemy_surface.set_alpha(alpha)
    screen.blit(enemy_surface, (x, y))
    
# Função para atirar a bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + playerImg.get_width() // 2 - bulletImg.get_width() // 2, y))
    
# Função para detectar colisão entre objetos
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Função para reiniciar o jogo
def reset_game():
    global score_value, playerX, playerY, bulletX, bulletY, bullet_state, player_lives, current_stage, enemies_destroyed
    score_value = 0
    playerX = 370
    playerY = 480
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    player_lives = 3
    current_stage = 0
    enemies_destroyed = 0
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
    
# Define a velocidade de interpolação para movimento suave
interpolation_speed = 0.1

# Variáveis de controle do loop principal
running = True
game_started = False
game_over = False

# Variáveis para animação de explosão
exploding_enemies = {}
EXPLOSION_DURATION = 30  # Duração da explosão em frames

# Loop principal do jogo
while running:
    if not game_started:
        # Mostra a tela inicial se o jogo não começou
        draw_initial_screen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    # Reinicia a fase atual
                    reset_game()
    else:
        # Limpa a tela com cor preta
        screen.fill((0,0,0))
        # Desenha o fundo da fase atual
        screen.blit(stage_backgrounds[current_stage], (0, 0))
        
        # Processa eventos do pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Verifica se está esperando para iniciar próxima fase
                    if waiting_for_next_stage:
                        waiting_for_next_stage = False
                        
                    # Tiro normal do jogo
                    elif bullet_state == "ready":
                        laser = mixer.Sound('./assets/sound/laser.wav')
                        laser.set_volume(0.5)  # 70% do volume original
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
            # Obtém a posição do mouse
            mouseX, mouseY = pygame.mouse.get_pos()
            
            # Move o jogador suavemente em direção ao mouse
            playerX += (mouseX - playerX - playerImg.get_width() // 2) * interpolation_speed
            playerY += (mouseY - playerY - playerImg.get_height() // 2) * interpolation_speed
            
            # Mantém o jogador dentro dos limites da tela
            playerX = max(0, min(playerX, 736))
            playerY = max(0, min(playerY, 536))
            
            # Processa movimento e colisões dos inimigos
            for i in range(num_of_enemies):
                if i in exploding_enemies:
                    # Continua a animação de explosão
                    exploding_enemies[i]['timer'] += 1
                    alpha = int(255 * (1 - exploding_enemies[i]['timer'] / EXPLOSION_DURATION))
                    burst(enemyX[i], enemyY[i], alpha)
                    enemy(enemyX[i], enemyY[i], i, alpha)
                    
                    if exploding_enemies[i]['timer'] >= EXPLOSION_DURATION:
                        # Reposiciona o inimigo após a explosão
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)
                        del exploding_enemies[i]
                    continue
                
                # Verifica condição de fim de jogo
                if enemyY[i] > 440:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    game_over = True
                    break
                
                # Move os inimigos
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]
                    
                # Verifica colisão entre bala e inimigo
                collision_bullet = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision_bullet and bullet_state == "fire":
                    explosion = mixer.Sound('./assets/sound/explosion.wav')
                    explosion.set_volume(0.5)  # 70% do volume original
                    explosion.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    enemies_destroyed += 1  # Incrementa o contador de inimigos destruídos

                    # Inicia animação de explosão
                    exploding_enemies[i] = {'timer': 0}

                    # Verifica se é hora de mudar de fase
                    if enemies_destroyed >= 15 and not transitioning:
                        current_stage = (current_stage + 1) % len(stage_backgrounds)
                        transitioning = True
                        transition_alpha = 0
                        transition_direction = 1
                        transition_start_time = pygame.time.get_ticks()

                    # Desenha a transição de fase se necessário
                    draw_transition()

                # Verifica colisão entre inimigo e jogador
                collision_player = isCollision(enemyX[i], enemyY[i], playerX, playerY)
                if collision_player:
                    explosion_sound = mixer.Sound('./assets/sound/explosion.wav')
                    explosion_sound.set_volume(0.7)  # 70% do volume original
                    explosion_sound.play()
                    player_lives -= 1
                    if player_lives <= 0:
                        for j in range(num_of_enemies):
                            enemyY[j] = 2000
                        game_over = True
                        break
                    else:
                        # Inicia efeito de piscar
                        player_blinking = True
                        player_blink_start = pygame.time.get_ticks()
                        # Reposiciona o inimigo
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i)
                
            # Processa movimento da bala
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"
            
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change
            
            # Processa efeito de piscar do jogador
            if player_blinking:
                current_time = pygame.time.get_ticks()
                if current_time - player_blink_start < player_blink_duration:
                    if (current_time // player_blink_interval) % 2 == 0:
                        player(playerX, playerY)
                else:
                    player_blinking = False
            else:
                player(playerX, playerY)
            
            # Mostra pontuação e vidas
            show_score(textX, textY)
        else:
            # Mostra tela de fim de jogo
            game_over_text()
        
        # Atualiza a tela
        pygame.display.update()
        clock.tick(60)  # Limita FPS a 60
