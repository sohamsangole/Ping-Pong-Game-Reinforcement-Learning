import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from PingPongGame import PingPong

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(4, 256, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.epsilon = 1  # Initial exploration rate
        self.epsilon_decay = 0.995  # Decay rate for exploration
        self.min_epsilon = 0.01  # Minimum exploration rate


    def get_state(self, game):
        ball_x = game.ball.x
        ball_y = game.ball.y
        player1_y = game.player_pos1.y
        player2_y = game.player_pos2.y

        state = [ball_x,ball_y,player1_y,player2_y]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay  # Decay epsilon

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice([0, 1, 2], p=[1/3, 1/3, 1/3])  # Random action
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            return torch.argmax(prediction).item()

def train():
    record = 0
    agent = Agent()
    game = PingPong()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            print('Game', agent.n_games, 'Score', score, 'Record:', record)



if __name__ == '__main__':
    train()