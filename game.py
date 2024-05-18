import pygame
from pygame import mixer

mixer.init() 
paddle_hit_sound = mixer.Sound("sound1.mp3")
wall_hit_sound = mixer.Sound("sound2.mp3")
background_music = mixer.music.load("A Lonely Cherry Tree.mp3")
mixer.music.set_volume(0.0) # 0.4 
mixer.music.play(-1) 
score1 = 0
score2 = 0

pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption('PingPong')
clock = pygame.time.Clock()
running = True
dt = 0
player_pos1 = pygame.Vector2(1 * screen.get_width() / 16, screen.get_height() / 2- 40)
player_pos2 = pygame.Vector2(15 * screen.get_width() / 16, screen.get_height() / 2 - 40)
ball = pygame.Vector2(1 * screen.get_width() / 2, screen.get_height() / 2)
speed = [-900,0]
font = pygame.font.Font(None, 74)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    pygame.draw.rect(screen, "blue", (player_pos1.x, player_pos1.y, 20, 80), 10,10)
    pygame.draw.rect(screen, "red", (player_pos2.x, player_pos2.y, 20, 80), 10,10)
    pygame.draw.circle(screen,"black",(ball.x, ball.y),10)
    pygame.draw.line(screen, "black", (screen.get_width() // 2, 0), (screen.get_width() // 2, screen.get_height()), 2)
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos1.y -= 800 * dt
    if keys[pygame.K_s]:
        player_pos1.y += 800 * dt

    player_pos2.y = ball.y - 40

    player_pos1.y = max(0, min(player_pos1.y, screen.get_height() - 80))
    player_pos2.y = max(0, min(player_pos2.y, screen.get_height() - 80))

    ball += pygame.Vector2(speed[0] * dt, speed[1] * dt)


    if ball.y <= 0 or ball.y >= screen.get_height():
        speed[1] = -speed[1]
        # wall_hit_sound.play()

    # Ball collision with player 1's paddle
    if (ball.x - 10 <= player_pos1.x + 20 and player_pos1.y <= ball.y <= player_pos1.y + 80):
        if speed[0] < 0:  # Ensure the paddle hit is only processed once per collision
            speed[0] = -speed[0]
            offset = (ball.y - player_pos1.y) - 40  # 40 is half the paddle height
            speed[1] = offset * 25  # Adjust reflection angle
            # paddle_hit_sound.play()

    # Ball collision with player 2's paddle
    if (ball.x + 10 >= player_pos2.x and player_pos2.y <= ball.y <= player_pos2.y + 80):
        if speed[0] > 0:  # Ensure the paddle hit is only processed once per collision
            speed[0] = -speed[0]
            offset = (ball.y - player_pos2.y) - 40  # 40 is half the paddle height
            speed[1] = offset * 25  # Adjust reflection angle

    # Check for scoring
    if ball.x < player_pos1.x - 30:
        score2 += 1
        ball = pygame.Vector2(1 * screen.get_width() / 2, screen.get_height() / 2)
        player_pos1.y = screen.get_height() // 2 - 40
        player_pos2.y = screen.get_height() // 2 - 40
        speed = [900, 0]
        
    if ball.x > player_pos2.x + 30:
        score1 += 1
        ball = pygame.Vector2(1 * screen.get_width() / 2, screen.get_height() / 2)
        player_pos1.y = screen.get_height() // 2 - 40
        player_pos2.y = screen.get_height() // 2 - 40
        speed = [-900, 0]

    # Render the scores
    score_text = font.render(f"{score1} - {score2}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(screen.get_width() / 2, 50))
    screen.blit(score_text, text_rect)

    pygame.display.flip()
    clock.tick(60)
    dt = clock.tick(60) / 1000
pygame.quit()