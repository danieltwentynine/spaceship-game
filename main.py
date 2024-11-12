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
num_of_enemies = 8

# Inicializa cada inimigo com posições e velocidades aleatórias
for i in range(num_of_enemies):
    enemyImg.append(pygame.transform.scale(pygame.image.load('./assets/enemies/enemy.png'), (60, 60)))
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

# Variável para controlar o estado de pausa
paused = False

# Função para mostrar a tela de pausa
def pause_screen():
    # Desenha o fundo da tela de pausa
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # Título de pausa
    pause_title = go_font.render("PAUSA", True, (255, 255, 255))
    pause_rect = pause_title.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(pause_title, pause_rect)
    
    # Instruções para retomar/sair
    resume_text = font.render("Pressione ESC para Retomar", True, (255, 255, 255))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, 300))
    screen.blit(resume_text, resume_rect)
    
    quit_text = font.render("Pressione Q para Sair", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, 350))
    screen.blit(quit_text, quit_rect)

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
    # Título de game over
    if boss_hits >= BOSS_HIT_LIMIT:  # Verifica se o jogador derrotou o chefão
        over_text = go_font.render("VOCÊ VENCEU!", True, (255, 255, 255))
    else:
        over_text = go_font.render("GAME OVER", True, (255, 255, 255))
    over_rect = over_text.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(over_text, over_rect)
    
    # Pontuação final
    final_score = font.render(f"Pontuação Final: {score_value}", True, (255, 255, 255))
    score_rect = final_score.get_rect(center=(screen.get_width() // 2, 280))
    screen.blit(final_score, score_rect)
    
    # Instruções para reiniciar/sair
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
    
# Função de colisão para inimigos normais
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Função de colisão para o chefão
def isBossCollision(bossX, bossY, bulletX, bulletY):
    margin = 20
    boss_rect = pygame.Rect(
        bossX + margin, 
        bossY + margin, 
        bossImg.get_width() - 2*margin, 
        bossImg.get_height() - 2*margin
    )
    
    bullet_rect = pygame.Rect(
        bulletX,
        bulletY,
        bulletImg.get_width(),
        bulletImg.get_height()
    )
    
    return boss_rect.colliderect(bullet_rect)

# Função para reiniciar o jogo
def reset_game():
    global score_value, playerX, playerY, bulletX, bulletY, bullet_state, player_lives
    global boss_active, boss_hits, bossY, start_time, exploding_boss, game_started

    # Reinicia variáveis do jogador
    score_value = 0
    playerX = 370
    playerY = 480
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    player_lives = 3

    # Reinicia variáveis do chefão
    boss_active = False
    boss_hits = 0
    bossY = -200
    exploding_boss = None

    # Reinicia o tempo para controlar o surgimento do chefão
    start_time = pygame.time.get_ticks()

    # Reinicia posição dos inimigos
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
EXPLOSION_DURATION = 30  # Duração da explosão dos inimigos normais em frames
BOSS_EXPLOSION_DURATION = 10  # Duração reduzida para a explosão do chefão em frames

# Variáveis do chefão
bossImg = pygame.image.load('./assets/enemies/boss.png')
bossImg = pygame.transform.scale(bossImg, (200, 200))
bossX = 300
bossY = -200
bossY_change = 4
boss_active = False
boss_hits = 0
BOSS_HIT_LIMIT = 10

# Adicionar novas variáveis para movimento triangular do chefão
bossX_change = 5
boss_moving_right = True
boss_top_y = 50  # Ponto mais alto do triângulo
boss_bottom_y = 240  # Ponto mais baixo do triângulo

# Variáveis para animação de explosão
exploding_boss = None
EXPLOSION_DURATION = 30  # Duração da explosão em frames

# Função para desenhar o chefão
def boss(x, y):
    screen.blit(bossImg, (x, y))

# Variável para controlar o tempo de jogo
start_time = pygame.time.get_ticks()

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
    elif paused:
        # Mostra a tela de pausa
        pause_screen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Retoma o jogo
                elif event.key == pygame.K_q:
                    running = False  # Sai do jogo
    else:
        # Limpa a tela com cor preta
        screen.fill((0,0,0))
        # Desenha o fundo
        screen.blit(background, (0, 0))
        
        # Processa eventos do pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Verifica se o jogo acabou
                if game_over:
                    if event.key == pygame.K_r:  # Tecla R para reiniciar
                        game_over = False
                        reset_game()  # Reinicia completamente o jogo
                    elif event.key == pygame.K_q:  # Tecla Q para sair
                        running = False
                else:
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            laser = mixer.Sound('./assets/sound/laser.wav')
                            laser.set_volume(0.5)
                            laser.play()
                            bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                            bulletY = playerY
                            fire_bullet(bulletX, bulletY)
                    elif event.key == pygame.K_ESCAPE:
                        paused = True  # Pausa o jogo

            # Adiciona o evento de clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if bullet_state == "ready":
                        laser = mixer.Sound('./assets/sound/laser.wav')
                        laser.set_volume(0.5)
                        laser.play()
                        bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                        bulletY = playerY
                        fire_bullet(bulletX, bulletY)

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
                # Move os inimigos
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]

                if i in exploding_enemies:
                    exploding_enemies[i]['timer'] += 1
                    alpha = int(255 * (1 - exploding_enemies[i]['timer'] / EXPLOSION_DURATION))
                    burst(enemyX[i], enemyY[i], alpha)
                    enemy(enemyX[i], enemyY[i], i, alpha)
                    
                    if exploding_enemies[i]['timer'] >= EXPLOSION_DURATION:
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)
                        del exploding_enemies[i]
                    continue
                
                # Verifica colisão entre bala e inimigo
                collision_bullet = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision_bullet and bullet_state == "fire":
                    explosion = mixer.Sound('./assets/sound/explosion.wav')
                    explosion.set_volume(0.7)
                    explosion.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    exploding_enemies[i] = {'timer': 0}

                # Verifica colisão entre inimigo e jogador
                collision_player = isCollision(enemyX[i], enemyY[i], playerX, playerY)
                if collision_player:
                    explosion_sound = mixer.Sound('./assets/sound/explosion.wav')
                    explosion_sound.set_volume(0.7)
                    explosion_sound.play()
                    player_lives -= 1
                    if player_lives <= 0:
                        for j in range(num_of_enemies):
                            enemyY[j] = 2000
                        game_over = True
                        break
                    else:
                        player_blinking = True
                        player_blink_start = pygame.time.get_ticks()
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

            # Verifica se 10 segundos se passaram para ativar o chefão
            if not boss_active and (pygame.time.get_ticks() - start_time) > 20000:
                boss_active = True
                bossY = 0  # Inicia o chefão na parte superior da tela

            if boss_active:
                if exploding_boss:
                    exploding_boss['timer'] += 1
                    alpha = int(255 * (1 - exploding_boss['timer'] / BOSS_EXPLOSION_DURATION))
                    burst(bossX, bossY, alpha)
                    
                    if exploding_boss['timer'] >= BOSS_EXPLOSION_DURATION:
                        exploding_boss = None
                        if boss_hits >= BOSS_HIT_LIMIT:  # Chefão foi derrotado
                            boss_active = False
                            bossY = -200
                            game_over = True
                            # Limpa a tela
                            screen.fill((0, 0, 0))
                            screen.blit(background, (0, 0))
                            # Mostra a tela de game over
                            game_over_text()
                else:
                    # Movimento triangular do chefão
                    if boss_moving_right:
                        bossX += bossX_change
                        if bossY < boss_bottom_y:
                            bossY += bossY_change
                        if bossX >= 600:
                            boss_moving_right = False
                    else:
                        bossX -= bossX_change
                        if bossY > boss_top_y:
                            bossY -= bossY_change
                        if bossX <= 0:
                            boss_moving_right = True
                    
                    boss(bossX, bossY)

                    if bullet_state == "fire":
                        collision_boss = isBossCollision(bossX, bossY, bulletX, bulletY)
                        if collision_boss:
                            explosion = mixer.Sound('./assets/sound/explosion.wav')
                            explosion.set_volume(0.7)
                            explosion.play()
                            bulletY = 480
                            bullet_state = "ready"
                            boss_hits += 1
                            exploding_boss = {'timer': 0}

        else:
            # Limpa a tela
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            game_over_text()
        
        # Atualiza a tela
        pygame.display.update()
        clock.tick(60)  # Limita FPS a 60