"""Thanks to Marcos Maximo for the DQN implementation"""

import collections
import random
import numpy as np
from tensorflow.keras import activations, losses, optimizers, layers
from tensorflow.keras.models import Sequential

from snek.simulation.agent import Agent
from snek.simulation.consts import Move

# Inherited Deep Q Agent
class DQNAgent(Agent):
    def __init__(
            self,
            state_size,
            action_size,
            gamma=0.95,
            epsilon=0.5,
            epsilon_min=0.01,
            epsilon_decay=0.995,
            learning_rate=0.0005,
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
        """
        Creates the neural network model with off-policy training.
        The NN calculates the next state.
        """
        model = Sequential([
            layers.Dense(128, activation=activations.relu, input_shape=self.state_size),
            layers.Dense(128, activation=activations.relu),
            layers.Dense(128, activation=activations.relu),
            layers.Dense(self.action_size, activation=activations.linear),
        ], name='dqn-agent')
        model.compile(loss=losses.mse, optimizer=optimizers.legacy.Adam(learning_rate=self.learning_rate))
        return model

    def replay(self, batch_size):
        """Episode replay for Q Learning
        
        :type batch_size: int
        """
        
        # Do not replay until buffer is full
        if len(self.replay_buffer) < batch_size:
            return
        
        minibatch = random.sample(self.replay_buffer, batch_size)
        states = np.array([sample[0] for sample in minibatch])
        actions = np.array([sample[1] for sample in minibatch])
        actions_idx = np.array([self.moves.index(action) for action in actions])
        rewards = np.array([sample[2] for sample in minibatch])
        next_states = np.array([sample[3] for sample in minibatch])
        dones = np.array([sample[4] for sample in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma * np.amax(self.model.predict_on_batch(next_states), axis=1) * (1-dones)
        current_targets = self.model.predict_on_batch(states)

        idx = np.array(list(range(batch_size)))
        current_targets[[idx], [actions_idx]] = targets

        self.model.fit(states, current_targets, epochs=1, verbose=0)

    def load(self, name):
        """Load previously trained model."""
        self.model.load_weights(name)

    def save(self, name):
        """Save model weights"""
        self.model.save_weights(name)

    def update_epsilon(self):
        """Epsilon scheduling, until minimum epsilon is reached"""
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min

    def interact(self, state):
        """
        Interact with game, changing direction based on learned policy.
        Epsilon is set in order to enable exploration.

        :param state: state vector with 12 features
        :type state: np array
        """
        if np.random.rand() < self.epsilon:
            self.next_direction = self.moves[random.randrange(self.action_size)]
            return

        actions = self.model.predict(state, verbose=0)
        actions = actions.reshape(-1)
        idx = np.argmax(actions)
        self.next_direction = self.moves[idx]

    def update(self, x: int, y: int, on_apple: bool) -> bool:
        """Update agent position."""
        game_over = super().update(x, y, on_apple)
        return game_over

    def train(self, state, action, reward, next_state, done):
        """Train agent using episode replay."""
        self.replay_buffer.append((state, action, reward, next_state, done))
        if len(self.replay_buffer) > 2 * self.batch_size:
            self.replay(self.batch_size)
