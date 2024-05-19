import pygame
import random

pygame.init()
pygame.display.set_caption('PING - PONG')

class PingPong:
    def __init__(self, w=720, h=720):
        pygame.init()
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('PingPong')
        self.dt = 0
        self.player_pos1 = pygame.Vector2(1 * self.w / 16, self.h / 2 - 40)
        self.player_pos2 = pygame.Vector2(15 * self.w / 16, self.h / 2 - 40)
        self.ball = pygame.Vector2(1 * self.w / 2, self.h / 2)
        self.speed = [-900, 0]
        self.font = pygame.font.Font(None, 37)
        self.score1 = 0
        self.score2 = 0
        self.running = True
        self.reward1_num = 0
        self.reward2_num = 0
        self.reward3_num = 0

    def reset(self):
        self.player_pos1 = pygame.Vector2(1 * self.w / 16, self.h / 2 - 40)
        self.player_pos2 = pygame.Vector2(15 * self.w / 16, self.h / 2 - 40)
        self.ball = pygame.Vector2(1 * self.w / 2, self.h / 2)
        self.speed = [-900, 0]

    def draw(self):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, "blue", (self.player_pos1.x, self.player_pos1.y, 20, 80), 10, 10)
        pygame.draw.rect(self.screen, "red", (self.player_pos2.x, self.player_pos2.y, 20, 80), 10, 10)
        pygame.draw.circle(self.screen, "black", (int(self.ball.x), int(self.ball.y)), 10)
        pygame.draw.line(self.screen, "black", (self.screen.get_width() // 2, 0),
                         (self.screen.get_width() // 2, self.screen.get_height()), 2)
        score_text = self.font.render(f"{self.score1} - {self.score2}", True, (0, 0, 0))
        reward1_text = self.font.render(f"Distance Reward: {self.reward1_num:.2f}", True, (0, 0, 0))
        reward2_text = self.font.render(f"Ball Hits Reward: {self.reward2_num:.2f}", True, (0, 0, 0))
        reward3_text = self.font.render(f"Point Loses Penalty: {self.reward3_num:.2f}", True, (0, 0, 0))
        text_rect = score_text.get_rect(center=(self.screen.get_width() / 2, 50))
        reward1_rect = reward1_text.get_rect(center=(7 * self.screen.get_width() / 9, 100))
        reward2_rect = reward2_text.get_rect(center=(7 * self.screen.get_width() / 9, 150))
        reward3_rect = reward3_text.get_rect(center=(7 * self.screen.get_width() / 9, 200))
        self.screen.blit(score_text, text_rect)
        self.screen.blit(reward1_text, reward1_rect)
        self.screen.blit(reward2_text, reward2_rect)
        self.screen.blit(reward3_text, reward3_rect)
        pygame.display.flip()

    def move_players(self,action):
        if action == 0:
            self.player_pos1.y -= 800 * self.dt
        elif action == 1:
            self.player_pos1.y += 800 * self.dt
        elif action == 2:
            pass
        
        self.player_pos2.y = self.ball.y - 40
        self.player_pos1.y = max(0, min(self.player_pos1.y, self.h - 80))
        self.player_pos2.y = max(0, min(self.player_pos2.y, self.h - 80))

        # distance = abs(self.player_pos1.y + 40 - self.ball.y)

    def move_paddles(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos1.y -= 800 * self.dt
        if keys[pygame.K_s]:
            self.player_pos1.y += 800 * self.dt
        
        number = random.randint(1, 12)
        if number <= 3:
            self.player_pos2.y = self.ball.y - 20
        elif number >= 4 and number < 8:
            self.player_pos2.y = self.ball.y - 40
        else:
            self.player_pos2.y = self.ball.y - 60
        self.player_pos1.y = max(0, min(self.player_pos1.y, self.h - 80))
        self.player_pos2.y = max(0, min(self.player_pos2.y, self.h - 80))

    def move_ball(self):
        self.ball += pygame.Vector2(self.speed[0] * self.dt, self.speed[1] * self.dt)

    def handle_collisions(self):
        if self.ball.y <= 0 or self.ball.y >= self.h:
            self.speed[1] = -self.speed[1]
        if (self.ball.x - 10 <= self.player_pos1.x + 20 and
                self.player_pos1.y <= self.ball.y <= self.player_pos1.y + 80):
            if self.speed[0] < 0:
                self.speed[0] = -self.speed[0]
                offset = (self.ball.y - self.player_pos1.y) - 40
                self.speed[1] = offset * 25
                self.score1 += 1
        if (self.ball.x + 10 >= self.player_pos2.x and
                self.player_pos2.y <= self.ball.y <= self.player_pos2.y + 80):
            if self.speed[0] > 0:
                self.speed[0] = -self.speed[0]
                offset = (self.ball.y - self.player_pos2.y) - 40
                self.speed[1] = offset * 25
                self.score2 += 1
                

    def check_scoring(self):
        if self.ball.x < self.player_pos1.x - 30:
            self.reset()
            self.speed = [900, 0]
            return True, True
        if self.ball.x > self.player_pos2.x + 30:
            self.reset()
            self.speed = [-900, 0]
            return True, False
        return False, False

    def run_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.dt = self.clock.tick(60) / 1000

            self.move_paddles()
            self.move_ball()
            self.handle_collisions()
            self.check_scoring()
            self.draw()

        pygame.quit()

    def play(self, action):
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.dt = clock.tick(60) / 1000
        self.move_players(action=action)
        self.move_ball()
        distance = abs(self.player_pos1.y + 40 - self.ball.y)  # 40 is the paddle half-height
        self.handle_collisions()
        game_over, you_lose = self.check_scoring()
        self.draw()
        score = self.score1
        reward = 0
        reward1 = 10 * (320 - distance) / 320
        reward2 = 0
        reward3 = 0
        # Ball Hits Paddle        
        if (self.ball.x - 10 <= self.player_pos1.x + 20 and self.player_pos1.y <= self.ball.y <= self.player_pos1.y + 80):
                reward2 = 10 
        else:
            reward2 = 0

        if you_lose:
            reward3 = -10
        else:
            reward3 = 0

        if game_over:
            self.reset_score()

        reward = reward1 + reward2 + reward3
        self.reward1_num = reward1
        self.reward2_num = reward2
        self.reward3_num = reward3
        # print(self.reward_num)
        return reward, game_over, score
    
    def reset_score(self):
        self.score1 = 0
        self.score2 = 0

    



# game = PingPong()
# game.run_game()