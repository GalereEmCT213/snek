"""Thanks to Marcos Maximo for the DQN implementation"""

import collections
import random
import pygame
import numpy as np
from tensorflow.keras import activations, losses, optimizers, layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import InceptionV3

from snek.learning.dql_agent import DQNAgent
from snek.simulation.game import Game
from snek.simulation.agent import Agent
from snek.simulation.consts import Move
from snek.simulation.consts import (
    AGENT_SIZE_X,
    AGENT_SIZE_Y, 
    GRID_SIZE_X,
    GRID_SIZE_Y
)

# Inherited Deep Q Agent
class CNNGame(Game):
    def _generate_state(self):
        """
        Generates the state (image in array) based on actual game situtaion

        :return: array with shape Game.window = (agent.size_x*grid.x, agent.size_y*grid.y)
        :type return: np array
        """
        game_prtsc = pygame.surfarray.array3d(self.game_window)
        game_prtsc = np.reshape(game_prtsc, (1,AGENT_SIZE_X*GRID_SIZE_X,AGENT_SIZE_Y* GRID_SIZE_Y,3))
        return game_prtsc


class CNNAgent(DQNAgent):          
    def make_model(self):
        """
        Creates the convolutional network model with off-policy training.
        The CNN calculates the next state.
        """
        transfer_model = InceptionV3(
            include_top=False, 
            weights='imagenet', 
            input_shape=(AGENT_SIZE_X*GRID_SIZE_X, AGENT_SIZE_Y* GRID_SIZE_Y, 3),
            )
        for layer in transfer_model.layers:
            layer.trainable = False
        transfer_model.summary()

        model = Sequential()
        model.add(transfer_model)
        model.add(layers.GlobalAveragePooling2D()),
        model.add(layers.Dense(128, activation=activations.relu)),
        model.add(layers.Dense(64, activation=activations.relu)),
        model.add(layers.Dense(self.action_size, activation=activations.linear)),
            # layers.AveragePooling2D(pool_size=(self.size_x, self.size_y), strides=(self.size_x, self.size_y)),
            # layers.Convolution2D(32, (8, 8), strides=(4, 4), padding='same', activation=activations.relu),
            # layers.Convolution2D(64, (2, 2), strides=(2, 2), activation=activations.relu),
            # layers.Convolution2D(64, (1, 1), strides=(2, 2), activation=activations.relu),
        model.compile(loss=losses.mse, optimizer=optimizers.legacy.Adam(learning_rate=self.learning_rate))
        return model