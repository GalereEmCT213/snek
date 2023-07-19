from collections import deque
from tensorflow.keras import optimizers, activations, losses
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import pygame
import random
import numpy as np

from snek.simulation.consts import Move


class Agent:
    def __init__(self, x: int = 0, y: int = 0, direction: Move = Move.R, initial_size: int = 5):
        self.initial_size = initial_size
        self.x, self.y = x, y
        self.body = deque((x + i, y + 5) for i in reversed(range(initial_size)))
        self.size_x, self.size_y = (10, 10)
        self.sprites = deque(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y) for x, y in self.body)
        self.initial_direction = direction
        self.direction = direction
        self.next_direction = direction

    def interact(self):
        """Agent interaction with world.

        Here, the agent takes decision from which direction it's going to choose. For the gameplay, it just
        looks for input key press. However, for AI agent, this method should decide the best next move.
        TODO: implement the interact for the AI agent.
        """

        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            match event.key:
                case pygame.K_UP:
                    self.next_direction = Move.U
                case pygame.K_DOWN:
                    self.next_direction = Move.D
                case pygame.K_LEFT:
                    self.next_direction = Move.L
                case pygame.K_RIGHT:
                    self.next_direction = Move.R

    def update(self, x: int, y: int, on_apple: bool) -> bool:
        """Update position.

        Updates the agent position based on the interaction with world. Updates both body position and sprites.
        """
        if not on_apple:
            self.body.pop()
            self.sprites.pop()

        self.x, self.y = x, y
        self.body.appendleft((x, y))
        self.sprites.appendleft(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y))

        return self.body[0] in list(self.body)[1:]  # Memory usage?

    def validate_next_move(self) -> bool:
        match self.direction:
            case Move.R: return self.next_direction != Move.L
            case Move.L: return self.next_direction != Move.R
            case Move.U: return self.next_direction != Move.D
            case Move.D: return self.next_direction != Move.U
        return True

    def next_move(self) -> tuple[int, int]:
        """Agent next move based on direction and location."""
        if self.validate_next_move():
            self.direction = self.next_direction

        x, y = self.body[0]
        vx, vy = self.direction.value

        return x+vx, y+vy

    def init(self):
        self.direction = self.initial_direction
        self.next_direction = self.initial_direction
        self.body = deque((self.x + i, self.y + 5) for i in reversed(range(self.initial_size)))
        self.sprites = deque(pygame.Rect(x*self.size_x, y*self.size_y, self.size_x, self.size_y) for x, y in self.body)


class RandomAgent(Agent):
    def __init__(self, *args, epsilon: float = 0.1, **kwargs):
        self.epsilon = epsilon
        super().__init__(*args, **kwargs)

    def interact(self):
        if random.random() < self.epsilon:
            self.next_direction = random.choice([Move.L, Move.R, Move.D, Move.U])


class DQNAgent(Agent):
    def __init__(
            self,
            *args,
            state_size: int = 12,
            action_size: int = len(Move),
            gamma: float = 0.95,
            epsilon: float = 0.5,
            epsilon_min=0.01,
            epsilon_decay=0.98,
            learning_rate: float = 0.001,
            buffer_size: int = 4098,
            **kwargs
        ):
        self.state_size = state_size
        self.action_size = action_size
        self.replay_buffer = deque(maxlen=buffer_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.moves = list(Move)
        self.model = self.make_model()
        self.state = (self.x, self.y, False)
        super().__init__(*args, **kwargs)

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

    def save(self, name):
        self.model.save_weights(name)

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min

    def interact(self):
        if np.random.rand() < self.epsilon:
            self.next_direction = random.choice([Move.L, Move.R, Move.D, Move.U])
        else:
            actions = self.model.predict(self.state)
            best_action = np.argmax(actions)
            self.next_direction = self.moves[best_action]

    def update(self, x: int, y: int, on_apple: bool, reward: int) -> bool:
        # previous_state = (self.x, self.y, self.on_apple)
        # next_state = (x, y, on_apple)

        next_state = (x, y, on_apple)
        game_over = super().update(x, y, on_apple)
        self.replay_buffer.append((self.state, self.next_direction, reward, next_state, game_over))
        self.state = next_state

        # Change state (x, y, on_apple) to state properly
        # self.replay_buffer.append((, self.next_direction, reward, next_state, game_over))

        return game_over
