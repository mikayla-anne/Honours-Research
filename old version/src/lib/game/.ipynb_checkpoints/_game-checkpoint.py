#!/usr/bin/env python3

from os import write
import pygame
## We will use persistent data structures because we want fast
## immutable game states
from pyrsistent import m, v, pmap, PRecord
import time
import csv
import numpy as np


csv_save_a = open('acts-t.csv', 'w', encoding='UTF8', newline='')
writer_a = csv.writer(csv_save_a)

csv_save_b = open('check-t.csv', 'w', encoding='UTF8', newline='')
writer_b = csv.writer(csv_save_b)


predicted_move = -1
actual_move = -1

class Agent:
    def __init__(self):
        pass

    def decide(self, state):
        """Main decision function for the agent. Returns the action that the
        agent decides for the current player to perform.

        Note that the available actions at a given GameState is
        accessed via `state.actions`.

        :param GameState state: The current state of the game.
        :returns action: The desired action that the player will perform.

        """
        raise NotImplementedError

    def learn(self, states, player_id):
        print('in')
        """Optional function. In the special case that the agent has an
        evaluation function that it is actively learning, this
        function exists as a way of 'retrospectively' learning.

        For now, ignore this function.

        :param states: List of states that the game went through,
                       where states[0] is the initial state.
        """
        pass


class Game:
    def __init__(self, game_type, agents, display=False):
        self.game_type = game_type
        self.agents = list(agents)
        self.display = display
        if display:
            pygame.init()
            self.screen = pygame.display.set_mode((672, 480))

    def run(self, play_again='query', speed=2):
        # print('in run')

        num_games = 1000

        csv_save = open('savingprobs-t.csv', 'w', encoding='UTF8', newline='')
        writer = csv.writer(csv_save)

        blue_score = 0
        red_score = 0

        # writer.writerow(['start time',time.time()]) 
        # writer.writerow(['type', 'MM'])
        # writer.writerow(['depth', '5'])
        
        # t
        for l in range(0,num_games): # num of games
            
            writer.writerow(['game',l]) 
            writer_b.writerow(['game',l]) 
            print('game ' , l)
            
            #print('in while' , l)
            #print('play again' , play_again)
            iterats, game_winner,times_actions = self._run_round(speed, actual_move, predicted_move)
            # writer.writerow(['iterations', iterats])
            # writer.writerow(['times of actions', times_actions])

            print(game_winner)
            
            if game_winner == 1:
                print('red')
                writer.writerow(['winner', '1'])
                red_score+=1
            elif game_winner == 2:
                writer.writerow(['winner', '0'])
                blue_score += 1
            else:
                writer.writerow(['winner', '-1'])
            

            #self._play_again()


            
            # if not play_again or play_again == 'query' and not :
            #     break
        
        # writer.writerow(['blue games won', blue_score])
        # writer.writerow(['red games won', red_score])
        # writer.writerow(['end time', time.time()])
        csv_save.close()

    def _run_round(self, speed, actual_move,predicted_move):
        
        state = self.game_type.init(self.agents)
        states = [state]
        i = np.random.choice([0,1])
        self._draw_state(state)
        if speed == 2:
            turn_wait = 0
            round_wait = 10
        elif speed == 1:
            turn_wait = 50
            round_wait = 100
        else:
            turn_wait = 500
            round_wait = 1000


        times_act = []
        num_iter = 0

        last_act_o = None
        last_act_m = None
        while not state.is_terminal:
            new_state = None
            i = (i + 1) % len(self.agents)
            # print('i' , i)
            while new_state == None:
                start_t = int(round(time.time() * 1000))
                agent = self.agents[i]
                # print("player check  " , i)
                # print('players    ' , state.players)
                st = time.time()
                action , pred = agent.decide(state,last_act_m,last_act_o)  # minimax / opponent goes here
                # print("current action  " , action)
                # print('')
                # print("me last action " , last_act_m)
                # print("opp last action  " , last_act_o)

                en = time.time()
                # print("player check " , i)

                if i == 1:
                    # print('in if , ' , i)
                    writer_a.writerow(['p1 act', action])
                    actual_move = action
                    # print(predicted_move)
                else:
                    # print('in else , ' , i)
                    # print('pred' , pred)
                    writer_a.writerow(['pred' , pred])
                    # print('act move' , actual_move)
                    # print('check ' , actual_move == predicted_move)
                    writer_b.writerow(['check', actual_move == predicted_move])
                    predicted_move = pred
                    # print('pred move' , predicted_move)

                    # times_act.append(action)

                
                # print('coords  ' , (state.players[i].x,state.players[i].y))
                # print(i , 'ACTION' , action)
                # print('act in game')
                # state = state.update_last_actions(action)
                if i == 0:
                    last_act_m = action
                elif i == 1:
                    last_act_o = action
                new_state = state.act(action)  # implement chosen action
                
                if not new_state:
                    print("Invalid action performed!")
            self._draw_state(new_state)
            # print('current player   ' , new_state.current_player)
            if new_state in states:
                print("State has been repeated! Therefore, game is over.")
                break
            states += [new_state]
            state = new_state
            end_t = int(round(time.time() * 1000))
            wait_time = turn_wait - (end_t - start_t)
            # print('wait time' , wait_time)
            # while True:
            #     pygame.event.clear()
            #     event = pygame.event.wait()
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
            #             break
            if wait_time > 0 and self.display:
                pygame.time.wait(wait_time)

            num_iter += 1

        
            
        for player_id, agent in enumerate(self.agents):
            print('for ' , player_id)
            agent.learn(states, player_id)
        pygame.time.wait(round_wait)
        
        # print(times_act)
        return num_iter,state.winner,times_act

    def _draw_state(self, state):
        if self.display:
            surf = state.draw()
            # surf = pygame.transform.scale(surf, (672, 480))
            self.screen.blit(surf, (0, 0))
            pygame.display.flip()

    def _play_again(self):
        font = pygame.font.SysFont("monospace", 32)
        font.set_bold(True)
        label = font.render("play again? (y/n)", 1, (255, 255, 255))
        window = (self.screen.get_width()/2 - 200, self.screen.get_height()/2 - 30, 400, 60)
        window_b = (window[0]-4, window[1]-4, window[2]+8, window[3]+8)
        pygame.draw.rect(self.screen, (255, 255, 255), window_b)
        pygame.draw.rect(self.screen, (0, 0, 0), window)
        self.screen.blit(label, (window[0]+18, window[1]+7))
        pygame.display.flip()
        while True:
            pygame.event.clear()
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False

class GameType:
    """A helper class that initializes the game state. Used as a class
    since the game type might have parameters."""
    def __init__(self):
        pass

    def init(self, agents):
        pass


class GameState(PRecord):
    """A recording of the current state of a game. The game state performs
    several functions: it contains information about the current game
    state, but also contains code for running the game via the "act"
    method. This enables the Game class to run the game in real time
    while also allowing agents to look into the future.

    When writing your agent, it should only access the functions given
    in this class.

    """

    @property
    def num_players(self):
        """Returns the number of players in the game."""
        pass

    @property
    def current_player(self):
        """Returns the ID of the current player of the game."""
        pass

    @property
    def is_terminal(self):
        """True if the game state is at a terminal node."""
        raise NotImplementedError

    @property
    def actions(self):
        """Returns the list of actions available at this state."""
        raise NotImplementedError

    def reward(self, player_id):
        """Returns the reward that the player receives at the end of the
        game.

        :param int player_id: The player id.
        :return: The reward for `player_id` if the state is terminal;
                 None otherwise.
        """
        raise NotImplementedError

    def act(self, action):
        """Returns the resultant GameState object when performing `action` in
        the current state. Since the GameState keeps track of the
        current player, there is no need to pass which player is
        performing the action.

        For further emphasis, note that this function is NOT
        DESTRUCTIVE! It returns a *new* game state for which `action`
        has been performed without changing anything in the current
        GameState object.

        You might be worried that this method will be
        inefficient. However, this class has been implemented as a
        *persistent* data structure using pyrsistent, which means that
        it has several memory- and time-based optimizations that make
        copying efficient. It will be worse than destructive updates,
        but significantly better than deep copying.

        :param Action action: The action to perform
        :return: A new GameState where action has been performed, or
                 None if the action is invalid.

        """
        raise NotImplementedError

    def _action_is_valid(self, action):
        if self.is_terminal:
            print("""ERROR: Player tried to perform an action in a terminal state. Make sure that you are performing actions solely in non-terminal states.""")
            return None

        if not action in self.actions:
            print("""ERROR: Player tried to perform an illegal action. Make sure that you only perform actions available in `state.actions`.

Action: {}
Allowed actions: {}""".format(action, self.actions))
            return None
        return self

    def draw(self):
        """Used internally for visualizing the state of the game in the Game
        class.

        :returns: A pygame.Surface image of the current game state.
        """
        raise NotImplementedError
