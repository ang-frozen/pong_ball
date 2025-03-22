import pygame
import os
import random
import time
import sys

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PONG GAME')
BG_COLOR = pygame.Color('gray12')
GRAY = (200, 200, 200)

# Ball and paddles
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT // 2 - 70, 10, 140)

# Speed settings
b_speed_x = 7 * random.choice((1, -1))
b_speed_y = 7 * random.choice((1, -1))
initial_speed_x = b_speed_x
initial_speed_y = b_speed_y
p_speed = 0
o_speed = 7
o_hit = 0
p_hit = 0

# Sound settings
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("hit.wav")  # Ensure you have hit.wav in the working directory
sound_on = True

# Sound toggle button
button_rect = pygame.Rect(WIDTH - 150, 20, 140, 40)
button_font = pygame.font.Font(None, 30)


def difficulty(screen, label_text):
    font = pygame.font.Font(None, 30)
    label_font = pygame.font.Font(None, 40)  
    WIDTH, HEIGHT = screen.get_size()
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive
    active = False
    user_text = ""
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((30, 30, 30))  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:  
                        return user_text  
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]  
                    else:
                        user_text += event.unicode  

        color = color_active if active else color_passive

        label_surface = label_font.render(label_text, True, (255, 255, 255))
        label_x = WIDTH // 2 - label_surface.get_width() // 2
        label_y = input_box.y - 50  
        screen.blit(label_surface, (label_x, label_y))

        pygame.draw.rect(screen, color, input_box, 2)

        text_surface = font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        pygame.display.flip()
        clock.tick(30)


def looser(who):
    global o_hit, p_hit
    lost = "Opponent has been defeated" if who == 1 else "You have been defeated"
    start_time = time.time()
    
    while (time.time() - start_time) < 6:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)
        font = pygame.font.Font(None, 40)
        text = font.render(f"{lost}. Game is starting in {5 - int(time.time() - start_time)}", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        text = font.render(f"Number of Hits [Player: {p_hit} Opponent: {o_hit}]", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)


def ball_restart(who=0):
    global p_speed, p_hit, o_hit, b_speed_x, b_speed_y, initial_speed_x, initial_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    b_speed_x, b_speed_y = initial_speed_x * random.choice((1, -1)), initial_speed_y * random.choice((1, -1))
    p_speed = 0
    looser(who)
    p_hit, o_hit = 0, 0


def ball_animation():
    global b_speed_x, b_speed_y, o_hit, p_hit, sound_on
    ball.x += b_speed_x
    ball.y += b_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        b_speed_y *= -1
    if ball.left <= 0:
        ball_restart(who=1)
    if ball.right >= WIDTH:
        ball_restart(who=0)
    if ball.colliderect(player) or ball.colliderect(opponent):
        b_speed_x *= -1.02
        b_speed_y *= 1.02
        if ball.colliderect(player):
            p_hit += 1
        else:
            o_hit += 1
        if sound_on:
            hit_sound.play()


def player_animation():
    player.y += p_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT


def opponent_animation():
    if abs(ball.centery - opponent.centery) > o_speed:  # Move only if needed
        if opponent.centery < ball.centery:
            opponent.y += min(o_speed, abs(ball.centery - opponent.centery))  # Move smoothly
        elif opponent.centery > ball.centery:
            opponent.y -= min(o_speed, abs(ball.centery - opponent.centery))


def draw_sound_button():
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    text = "Sound: ON" if sound_on else "Sound: OFF"
    text_surface = button_font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))

def points_counter():
    global p_hit, o_hit
    font = pygame.font.Font(None, 25)
    text = font.render(f"Player: {p_hit}", True, (236, 82, 40), None)
    t_r = text.get_rect()
    screen.blit(text, (WIDTH//2+t_r[2], t_r[3]))
    text = font.render(f"Opponent: {o_hit}", True, (239, 150, 81), None)
    t_r = text.get_rect()
    screen.blit(text, (WIDTH//2-1.5*t_r[2], t_r[3]))

level = int(difficulty(screen, "Set difficulty level from 1 to 10"))
level = max(1, min(10, level))  # Ensure valid range

reaction_speed = 0.1 * level  
o_speed = 4 + level  

start_time = time.time()
while (time.time() - start_time) < 6:
    screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 40)
    text = font.render(f"Game is starting in {5 - int(time.time() - start_time)}", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    clock.tick(60)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                p_speed += 10
            if event.key == pygame.K_UP:
                p_speed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                p_speed -= 10
            if event.key == pygame.K_UP:
                p_speed += 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                sound_on = not sound_on

    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, GRAY, player)
    pygame.draw.rect(screen, GRAY, opponent)
    pygame.draw.ellipse(screen, GRAY, ball)
    pygame.draw.aaline(screen, GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    points_counter()
    draw_sound_button()

    pygame.display.flip()
    clock.tick(60)
