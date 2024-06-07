import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 20
player_speed = 5
player_lives = 5
player_score = 0

# Bullet
bullet_width, bullet_height = 10, 30
bullet_speed = 10
bullets = []

# Enemy
enemy_width, enemy_height = 50, 50
enemy_speed = 3
enemies = []

# Font
font = pygame.font.Font(None, 36)

# Create functions for drawing player, bullets, enemies, and UI
def draw_player():
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def draw_ui():
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    score_text = font.render(f"Score: {player_score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 50))

# Main game loop
clock = pygame.time.Clock()

state = "START"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == "START" and event.key == pygame.K_SPACE:
                state = "PLAY"
            elif state == "GAME_OVER" and event.key == pygame.K_RETURN:
                state = "PLAY"
                player_lives = 3
                player_score = 0
                enemies.clear()
            elif state == "PLAY" and event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2,
                                            player_y - bullet_height, bullet_width, bullet_height))

    if state == "PLAY":
        screen.fill(BLACK)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Bullet movement and collision
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    player_score += 10

        # Enemy spawning
        if random.randint(0, 80) < 5:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy_y = random.randint(-50, -enemy_height)
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

        # Enemy movement and collision with player
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                player_lives -= 1
                enemies.remove(enemy)
                if player_lives == 0:
                    state = "GAME_OVER"

        draw_player()
        draw_bullets()
        draw_enemies()
        draw_ui()

    elif state == "GAME_OVER":
        screen.fill(BLACK)
        game_over_text = font.render("Game Over. Press ENTER.", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    elif state == "START":
        screen.fill(BLACK)
        start_text = font.render("Press SPACE to start the game.", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

