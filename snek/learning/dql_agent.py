"""Thanks to Marcos Maximo for the DQN implementation"""

import collections
import random
import numpy as np
from tensorflow.keras import activations, losses, optimizers, layers
from tensorflow.keras.models import Sequential

from snek.simulation.agent import Agent
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
            buffer_size=4098,
            batch_size=32
        ):
        self.state_size = state_size
        self.action_size = action_size
        self.replay_buffer = collections.deque(maxlen=buffer_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.moves = list(Move)
        self.model = self.make_model()
        super().__init__()
    
    def make_model(self):
        model = Sequential([
            layers.Dense(256, activation=activations.relu, input_shape=self.state_size),
            layers.Dense(self.action_size, activation=activations.relu),
        ], name='dqn-agent')
        model.compile(loss=losses.mse, optimizer=optimizers.legacy.Adam(learning_rate=self.learning_rate))
        model.summary()
        return model

    def replay(self, batch_size):
        minibatch = random.sample(self.replay_buffer, batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state, verbose=0)
            action_idx = self.moves.index(action)
            if not done:
                target[0][action_idx] = reward + self.gamma * np.max(self.model.predict(next_state, verbose=0)[0])
            else:
                target[0][action_idx] = reward
            # Filtering out states and targets for training
            states.append(state[0])
            targets.append(target[0])
        history = self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        # Keeping track of loss
        loss = history.history['loss'][0]
        # self.replay_buffer.clear()
        return loss

    def load(self, name):
        self.model.load_weights(name)

    def act(self, state):
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)
        
        actions = self.model.predict(state, verbose=0)
        actions = actions.reshape(-1)
        return np.argmax(actions)

    def save(self, name):
        self.model.save_weights(name)

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min
        print(self.epsilon)

    def interact(self, state):
        if np.random.rand() < self.epsilon:
            self.next_direction = self.moves[random.randrange(self.action_size)]
            return

        actions = self.model.predict(state, verbose=0)
        actions = actions.reshape(-1)
        idx = np.argmax(actions)
        self.next_direction = self.moves[idx]

    def update(self, x: int, y: int, on_apple: bool) -> bool:
        # previous_state = (self.x, self.y, self.on_apple)
        # next_state = (x, y, on_apple)
        game_over = super().update(x, y, on_apple)
        return game_over

        # Change state (x, y, on_apple) to state properly
        # 

    def train(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))
        if len(self.replay_buffer) > 2 * self.batch_size:
            self.replay(self.batch_size)
