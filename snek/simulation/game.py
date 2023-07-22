import pygame
import numpy as np

from snek.simulation.agent import Agent
from snek.simulation.grid import Grid
from snek.simulation.consts import Color, Move
from snek.simulation.score import Score
from snek.simulation.reward import Reward


def check_quit() -> bool:
    if pygame.event.get(eventtype=pygame.QUIT):
        pygame.quit()
        return False
    return True


class Game:
    def __init__(
            self, 
            agent: Agent, 
            grid: Grid, 
            reward: Reward = Reward(), 
            speed: int =15, 
            manual_end: bool = False):
        """
        Creates a game.

        :param speed: speed of the game execution
        :param manual_end: flag to control if the window will be maually closed
        :param reward: reward engine, used for DQLearning
        :type reward: Reward

        :param end_condition: control game regulation
        :type end_condition: bool
        :param time: count the ticks of game
        :type time: int
        :param score: enigne to mark the eaten apples
        :typer score: Score
        """
        self.agent = agent
        self.grid = grid
        self.reward = reward
        self.speed = speed
        self.manual_end = manual_end
        self.window = (agent.size_x*grid.x, agent.size_y*grid.y)
        self.background = Color.BLACK
        self.end_condition = False
        self.time = 0
        self.score = Score()
        self.cumulative_reward = 0
        self.apple = (self.grid.xa, self.grid.ya)

        pygame.init()
        self.game_window = pygame.display.set_mode(self.window)
        self.fps = pygame.time.Clock()
        pygame.display.init()
        pygame.display.set_caption('snek')

    def update(self):
        """
        Update the agent and the grid state in the game.
        Also measure the reward with the reward engine.
        """
        self.reward.old_pos = (self.agent.x, self.agent.y)
        x, y = self.agent.next_move()
        x, y, on_apple = self.grid.interact(x, y)
        if on_apple:
            self.apple = self.grid.generate_apple(self.agent.body)
            self.score.prize()
        self.end_condition = self.agent.update(x, y, on_apple)
        self.reward.reward_engine(tick=True, dead=self.end_condition, appl=on_apple, snake_body=self.agent.body, apple_pos=self.apple)
        self.cumulative_reward = self.agent.gamma * self.cumulative_reward + self.reward.reward

    def draw(self):
        """
        Draw the objects in the game's window
        """
        pygame.event.pump()
        self.game_window.fill(Color.BLACK.value)
        pygame.draw.rect(self.game_window, Color.RED.value, self.grid.apple)
        for sprite in self.agent.sprites:
            pygame.draw.rect(self.game_window, Color.GREEN.value, sprite)
        self.score.display(self.game_window)
        pygame.display.update()
        self.fps.tick(self.speed)
        self.time += 1

    def init(self):
        """
        Re-start the game configuration
        """
        self.agent.init(x=0, y=0)
        self.grid.init(self.agent.body)
        self.time = 0
        self.cumulative_reward = 0
        self.end_condition = False
        self.reward.init()
        self.score.init()
        self.apple = (self.grid.xa, self.grid.ya)


    def play(self, train=False):
        """
        Executes a game session

        :param train: states if the session is for training

        :return self.reward.history: reward sum of a game session
        :type self.reward.history: float
        :return self.time: cumulative time of a gam session
        :type self.time: int
        """
        self.init()
        state = self._generate_state()

        while not self.end_condition:
            self.agent.interact(state)
            self.update()
            next_state = self._generate_state()

            if train:
                action = self.agent.direction
                reward = self.reward.reward
                done = self.end_condition
                self.agent.train(state, action, reward, next_state, done)
            
            state = next_state
            self.draw()
            if not check_quit():
                break
        else:
            self.game_over()
        
        if train:
            self.agent.update_epsilon()

        return self.reward.history, self.time

    def game_over(self):
        """
        Print the Game Over advisement and quit the pygame 
        enviroment when the manual session end is settled
        """
        game_over_font = pygame.font.Font(None, 20)
        game_over_surface = game_over_font.render('Git Gud', True, Color.WHITE.value)
        game_over_rect = game_over_surface.get_rect(topleft = (0,35))
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        if self.manual_end:
            while not pygame.event.peek(pygame.KEYDOWN) and not pygame.event.peek(pygame.QUIT):
                pass
            pygame.quit()

    def _generate_state(self):
        """
        Generates the state vector based on actual game situation
        """
        ax, ay = self.apple
        hx, hy = self.agent.body[0]
        grid_x, grid_y = self.grid.x, self.grid.y

        # Check position of apple relative to the snake:
        apple_up = apple_down = apple_left = apple_right = 0

        apple_up = (hy > ay)
        apple_down = (hy < ay)
        apple_left = (hx > ax)
        apple_right = (hx < ax)

        # Check for walls:
        wall_up = wall_down = wall_left = wall_right = 0

        if hy == 0:
            wall_up, wall_down = 1, 0
        elif hy == grid_y - 1:
            wall_up, wall_down = 0, 1
        
        if hx == 0: 
            wall_left, wall_right = 1, 0
        elif hx == grid_x - 1:
            wall_left, wall_right = 0, 1

        # Check for body:
        body_up = body_down = body_left = body_right = 0

        for body in list(self.agent.body)[3:]:
            if (hy - body[1] <= 1 and hy > body[1] and hx == body[0]):
                body_up, body_down = 1, 0
            elif (body[1] - hy <= 1 and body[1] > hy and hx == body[0]):
                body_up, body_down = 0, 1

            if (hx - body[0] <= 1 and hx > body[0] and hy == body[1]):
                body_left, body_right = 1, 0
            elif (body[0] - hx <= 1 and body[0] > hx and hy == body[1]):
                body_left, body_right = 0, 1

        # Use wall and body check to check for obstacles nearby:
        obstacle_up = wall_up or body_up
        obstacle_down = wall_down or body_down
        obstacle_left = wall_left or body_left
        obstacle_right = wall_right or body_right

        # Direction check:
        direction_up = direction_down = direction_left = direction_right = 0

        match self.agent.direction:
            case Move.U: direction_up = 1
            case Move.D: direction_down = 1
            case Move.L: direction_left = 1
            case Move.R: direction_right = 1
 
        state = [apple_up, apple_down, apple_left, apple_right, \
                 obstacle_up, obstacle_down, obstacle_left, obstacle_right, \
                 direction_up, direction_down, direction_left, direction_right]
        return np.array([state])
    
    def _get_game_score(self):
        """
        Get game score when it is called
        """
        return self.score.score
