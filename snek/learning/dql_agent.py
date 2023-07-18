"""Thanks to Marcos Maximo for the DQN implementation"""

import collections
import random
import numpy as np
from tensorflow.keras import activations, losses, optimizers
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from snek.simulation import Agent
from snek.simulation.consts import Move

class DQNAgent(Agent):
    def __init__(
            self,
            state_size,
            action_size,
            gamma=0.95,
            epsilon=0.5,
            epsilon_min=0.01,
            epsilon_decay=0.98,
            learning_rate=0.001,
            buffer_size=4098
        ):
        self.state_size = state_size
        self.action_size = action_size
        self.replay_buffer = collections.deque(maxlen=buffer_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.moves = list(Move)
        self.model = self.make_model()
        super().__init__()
    
    def make_model(self):
        model = Sequential([
            Dense(256, input_dim=self.state_size, activation=activations.relu),
            Dense(256, activation=activations.relu),
            Dense(self.action_size, activation=activations.linear)
        ], name='dqn-agent')
        model.compile(loss=losses.mse, optimizer=optimizers.legacy.Adam(learning_rate=self.learning_rate))
        model.summary()
        return model

    def replay(self, batch_size):
        minibatch = random.sample(self.replay_buffer, batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if not done:
                target[0][action] = reward + self.gamma * np.max(self.model.predict(next_state)[0])
            else:
                target[0][action] = reward
            # Filtering out states and targets for training
            states.append(state[0])
            targets.append(target[0])
        history = self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        # Keeping track of loss
        loss = history.history['loss'][0]
        return loss

    def load(self, name):
        self.model.load_weights(name)

    def act(self, state):
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)
        
        actions = self.model.predict(state)
        actions = actions.reshape(-1)
        return np.argmax(actions)

    def save(self, name):
        self.model.save_weights(name)

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min

    def interact(self, state=None):
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)
        
        actions = self.model.predict(state)
        actions = actions.reshape(-1)
        idx = np.argmax(actions)
        self.next_direction = self.moves[idx]

    def update(self, x: int, y: int, on_apple: bool, reward: int) -> bool:
        # previous_state = (self.x, self.y, self.on_apple)
        # next_state = (x, y, on_apple)
        game_over = super().update(x, y, on_apple, reward)

        # Change state (x, y, on_apple) to state properly
        # self.replay_buffer.append((, self.next_direction, reward, next_state, game_over))

        return game_over