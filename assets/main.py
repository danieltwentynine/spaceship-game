# PyBag Compatible Space Invaders Game
import asyncio
import pygame
import random
import math
from pygame import mixer
import time

# Initialize pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Set window title
pygame.display.set_caption('Space Invaders')

# Load and set icon
try:
    icon = pygame.image.load('assets/player/nave.png')
    pygame.display.set_icon(icon)
except:
    pass  # Icon not critical for web version

# Load background
try:
    background = pygame.image.load('assets/backgrounds/background.png')
except:
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 50))  # Fallback dark blue background

# Player setup
try:
    playerImg = pygame.image.load('assets/player/nave.png')
    playerImg = pygame.transform.scale(playerImg, (80, 80))
except:
    # Fallback player image
    playerImg = pygame.Surface((80, 80))
    playerImg.fill((0, 255, 0))

playerX = 370
playerY = 480
playerX_change = 0
player_speed = 5
playerY_change = 0

# Enemy setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

# Initialize enemies
for i in range(num_of_enemies):
    try:
        enemy_surface = pygame.image.load('assets/enemies/enemy.png')
        enemy_surface = pygame.transform.scale(enemy_surface, (60, 60))
        enemyImg.append(enemy_surface)
    except:
        # Fallback enemy image
        enemy_surface = pygame.Surface((60, 60))
        enemy_surface.fill((255, 0, 0))
        enemyImg.append(enemy_surface)
    
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Bullet setup
try:
    bulletImg = pygame.image.load('assets/elements/bullet.png')
except:
    bulletImg = pygame.Surface((10, 20))
    bulletImg.fill((255, 255, 0))

bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Explosion animation setup
burst_images = []
for i in range(1, 6):
    try:
        burst_images.append(pygame.image.load(f'assets/elements/explosion-{i}.png'))
    except:
        # Fallback explosion image
        explosion_surface = pygame.Surface((60, 60))
        explosion_surface.fill((255, 100, 0))
        burst_images.append(explosion_surface)

burst_index = 0
burst_timer = 0
BURST_FRAME_DURATION = 3

# Explosion animation function
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
        burst_index = 0

# Score and UI setup
score_value = 0
font = pygame.font.Font(None, 32)  # Use default font for web compatibility
textX = 10
textY = 10
go_font = pygame.font.Font(None, 64)
GAME_FONT = pygame.font.Font(None, 20)
TITLE_FONT = pygame.font.Font(None, 32)
start_button = pygame.Rect(300, 400, 200, 50)

# Player lives and effects
player_lives = 3
player_blinking = False
player_blink_start = 0
player_blink_duration = 2000
player_blink_interval = 200

# Game state variables
paused = False
interpolation_speed = 0.1
running = True
game_started = False
game_over = False

# Explosion effects
exploding_enemies = {}
EXPLOSION_DURATION = 30
BOSS_EXPLOSION_DURATION = 10

# Boss setup
try:
    bossImg = pygame.image.load('assets/enemies/boss.png')
    bossImg = pygame.transform.scale(bossImg, (200, 200))
except:
    bossImg = pygame.Surface((200, 200))
    bossImg.fill((255, 0, 255))

bossX = 300
bossY = -200
bossY_change = 4
boss_active = False
boss_hits = 0
BOSS_HIT_LIMIT = 10
bossX_change = 5
boss_moving_right = True
boss_top_y = 50
boss_bottom_y = 240
exploding_boss = None
start_time = pygame.time.get_ticks()

# Sound functions with error handling
def play_sound(sound_path, volume=0.5):
    try:
        sound = mixer.Sound(sound_path)
        sound.set_volume(volume)
        sound.play()
    except:
        pass  # Sound not available

# Game functions
def pause_screen():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    pause_title = go_font.render("PAUSA", True, (255, 255, 255))
    pause_rect = pause_title.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(pause_title, pause_rect)
    
    resume_text = font.render("Pressione ESC para Retomar", True, (255, 255, 255))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, 300))
    screen.blit(resume_text, resume_rect)
    
    quit_text = font.render("Pressione Q para Sair", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, 350))
    screen.blit(quit_text, quit_rect)

def draw_initial_screen():
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
    if boss_hits >= BOSS_HIT_LIMIT:
        over_text = go_font.render("VOCÊ VENCEU!", True, (255, 255, 255))
    else:
        over_text = go_font.render("GAME OVER", True, (255, 255, 255))
    over_rect = over_text.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(over_text, over_rect)
    
    final_score = font.render(f"Pontuação Final: {score_value}", True, (255, 255, 255))
    score_rect = final_score.get_rect(center=(screen.get_width() // 2, 280))
    screen.blit(final_score, score_rect)
    
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

def reset_game():
    global score_value, playerX, playerY, bulletX, bulletY, bullet_state, player_lives
    global boss_active, boss_hits, bossY, start_time, exploding_boss, game_started

    score_value = 0
    playerX = 370
    playerY = 480
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    player_lives = 3

    boss_active = False
    boss_hits = 0
    bossY = -200
    exploding_boss = None

    start_time = pygame.time.get_ticks()

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)

def boss(x, y):
    screen.blit(bossImg, (x, y))

# Main game loop
async def main():
    global running, game_started, game_over, paused
    global playerX, playerY, bulletX, bulletY, bullet_state
    global score_value, player_lives, player_blinking, player_blink_start
    global boss_active, boss_hits, bossX, bossY, boss_moving_right, exploding_boss
    global exploding_enemies, start_time

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
                        reset_game()
        elif paused:
            pause_screen()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                    elif event.key == pygame.K_q:
                        running = False
        else:
            screen.fill((0,0,0))
            screen.blit(background, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if game_over:
                        if event.key == pygame.K_r:
                            game_over = False
                            reset_game()
                        elif event.key == pygame.K_q:
                            running = False
                    else:
                        if event.key == pygame.K_SPACE:
                            if bullet_state == "ready":
                                play_sound('assets/sound/laser.wav', 0.5)
                                bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                                bulletY = playerY
                                fire_bullet(bulletX, bulletY)
                        elif event.key == pygame.K_ESCAPE:
                            paused = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if bullet_state == "ready":
                            play_sound('assets/sound/laser.wav', 0.5)
                            bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                            bulletY = playerY
                            fire_bullet(bulletX, bulletY)

            if not game_over:
                mouseX, mouseY = pygame.mouse.get_pos()
                
                playerX += (mouseX - playerX - playerImg.get_width() // 2) * interpolation_speed
                playerY += (mouseY - playerY - playerImg.get_height() // 2) * interpolation_speed
                
                playerX = max(0, min(playerX, 736))
                playerY = max(0, min(playerY, 536))
                
                for i in range(num_of_enemies):
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
                    
                    collision_bullet = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                    if collision_bullet and bullet_state == "fire":
                        play_sound('assets/sound/explosion.wav', 0.7)
                        bulletY = 480
                        bullet_state = "ready"
                        score_value += 1
                        exploding_enemies[i] = {'timer': 0}

                    collision_player = isCollision(enemyX[i], enemyY[i], playerX, playerY)
                    if collision_player:
                        play_sound('assets/sound/explosion.wav', 0.7)
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
                    
                if bulletY <= 0:
                    bulletY = 480
                    bullet_state = "ready"
                
                if bullet_state == "fire":
                    fire_bullet(bulletX, bulletY)
                    bulletY -= bulletY_change
                
                if player_blinking:
                    current_time = pygame.time.get_ticks()
                    if current_time - player_blink_start < player_blink_duration:
                        if (current_time // player_blink_interval) % 2 == 0:
                            player(playerX, playerY)
                    else:
                        player_blinking = False
                else:
                    player(playerX, playerY)
                
                show_score(textX, textY)

                if not boss_active and (pygame.time.get_ticks() - start_time) > 20000:
                    boss_active = True
                    bossY = 0

                if boss_active:
                    if exploding_boss:
                        exploding_boss['timer'] += 1
                        alpha = int(255 * (1 - exploding_boss['timer'] / BOSS_EXPLOSION_DURATION))
                        burst(bossX, bossY, alpha)
                        
                        if exploding_boss['timer'] >= BOSS_EXPLOSION_DURATION:
                            exploding_boss = None
                            if boss_hits >= BOSS_HIT_LIMIT:
                                boss_active = False
                                bossY = -200
                                game_over = True
                                screen.fill((0, 0, 0))
                                screen.blit(background, (0, 0))
                                game_over_text()
                    else:
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
                                play_sound('assets/sound/explosion.wav', 0.7)
                                bulletY = 480
                                bullet_state = "ready"
                                boss_hits += 1
                                exploding_boss = {'timer': 0}

            else:
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))
                game_over_text()
            
            pygame.display.update()
            clock.tick(60)
            await asyncio.sleep(0)  # Essential for PyBag compatibility

if __name__ == "__main__":
    asyncio.run(main())