#!/usr/bin/env python3
from os import stat
from pyrsistent import PMap
import numpy as np
from collections import defaultdict

from src.lib.game.discrete_soccer import Action
from ...lib.game import Agent, RandomAgent, GameState


class MinimaxAgent(RandomAgent):
    """An agent that makes decisions using the Minimax algorithm, using a
    evaluation function to approximately guess how good certain states
    are when looking far into the future.

    :param evaluation_function: The function used to make evaluate a
        GameState. Should have the parameters (state, player_id) where
        `state` is the GameState and `player_id` is the ID of the
        player to calculate the expected payoff for.

    :param alpha_beta_pruning: True if you would like to use
        alpha-beta pruning.

    :param max_depth: The maximum depth to search using the minimax
        algorithm, before using estimates generated by the evaluation
        function.
    """

    def __init__(self, evaluate_function, alpha_beta_pruning=False, max_depth=5):
        super().__init__()
        self.evaluate = evaluate_function
        print('EVAL FUNCTION\n',evaluate_function)
        self.alpha_beta_pruning = alpha_beta_pruning
        self.max_depth = max_depth

    def decide(self, state: GameState):
        if state is None:
            print("STATE IS NONE")
        else:
            print("state is fine")
        # TODO: Implement this agent!
        #
        # Read the documentation in /src/lib/game/_game.py for
        # information on what the decide function does.
        #
        # Do NOT call the soccer evaluation function that you write
        # directly from this function! Instead, use
        # `self.evaluate`. It will behave identically, but will be
        # able to work for multiple games.
        #
        # Do NOT call any SoccerState-specific functions! Assume that
        # you can only see the functions provided in the GameState
        # class.
        #
        # If you would like to see some example agents, check out
        # `/src/lib/game/_agents.py`.

        if not self.alpha_beta_pruning:
            return self.minimax(state)

        else:
            return self.minimax_with_ab_pruning(state)

    def minimax(self, state: GameState):
        # This is the suggested method you use to do minimax.  Assume
        # `state` is the current state, `player` is the player that
        # the agent is representing (NOT the current player in
        # `state`!)  and `depth` is the current depth of recursion.
        # return super().decide(state)

        best_action = None
        best_score = float("-inf")
        for index, action in enumerate(state.actions):

            # print(str(action) + " score: " + str(self.evaluate(state.act(action), state.current_player)))
            new_state = state.act(action)
            if new_state is not None:
                # print(new_state)
                score = self.min_value(new_state, state.current_player)
                # score = self.evaluate(state.act(action), state.current_player)
                #print(str(action) + ": " + str(score))
                if score > best_score:
                    best_action = action
                    best_score = score
        return best_action

    def minimax_with_ab_pruning(self, state):
        print("WITH AB PRUNING")
        best_action = None
        best_score = float("-inf")
        for index, action in enumerate(state.actions):

            # print(str(action) + " score: " + str(self.evaluate(state.act(action), state.current_player)))
            new_state = state.act(action)
            if new_state is not None:
                # print(new_state)
                print(str(action))
                score = self.min_value(new_state, state.current_player, pruning=True, alpha=best_score, beta=float("inf"))
                # score = self.evaluate(state.act(action), state.current_player)
                print(str(action) + ": " + str(score))
                if score > best_score:
                    best_action = action
                    best_score = score
        return best_action

    def min_value(self, state: GameState, player, depth: int = 1, pruning: bool = False, alpha: float = float("-inf"),
                  beta: float = float("inf")):
        # TODO un-combine reward and evaluation
        # print(state)

        spaces = ""
        for i in range(0, depth):
            spaces += "    "

        # If at a terminal state, return the reward
        if state.is_terminal:
            return state.reward(player) + self.evaluate(state, player)
        # If we reached the max search depth, return the utility
        if depth >= self.max_depth:
            # print('EVAL SP\n', self.evaluate(state,player))
            return self.evaluate(state, player)

        smallest_score = float("inf")
        for index, action in enumerate(state.actions):
            new_state = state.act(action)
            if new_state is not None:
                #print(str(spaces) + str(alpha) + ", " + str(beta))
                #print(spaces + str(action))
                score = self.max_value(new_state, player, depth=depth + 1, pruning=pruning, alpha=alpha, beta=beta)
                #print(spaces + str(action) + ": " + str(score))
                if score < smallest_score:
                    #print(spaces + "New Smallest Score")
                    smallest_score = score
            if pruning:
                if smallest_score <= alpha:
                    #print(spaces + "pruned")
                    #print(spaces + "score: " + str(smallest_score) + " <= alpha: " + str(alpha))
                    return smallest_score

                beta = min(beta, smallest_score)
                #if smallest_score < beta:
                    #print(spaces + "Beta: " + str(beta))
        return smallest_score

    def max_value(self, state: GameState, player, depth: int = 1, pruning: bool = False, alpha: float = float("-inf"),
                  beta: float = float("inf")):
        # print(state)
        spaces = ""
        for i in range(0, depth):
            spaces += "    "
        # If at a terminal state, return the reward
        if state.is_terminal:
            return state.reward(player) + self.evaluate(state, player)
        # If we reached the max search depth, return the utility
        if depth >= self.max_depth:
            return self.evaluate(state, player)

        biggest_score = float("-inf")
        for index, action in enumerate(state.actions):
            new_state = state.act(action)
            if new_state is not None:
                #print(str(spaces) + str(alpha) + ", " + str(beta))
                #print(spaces + str(action))
                score = self.min_value(new_state, player, depth=depth + 1, pruning=pruning, alpha=alpha, beta=beta)
                #print(spaces + str(action) + ": " + str(score))
                if score > biggest_score:
                    #print(spaces + "New Biggest Score")
                    biggest_score = score
            if pruning:
                if biggest_score >= beta:
                    #print(spaces + "pruned")
                    #print(spaces + "score: " + str(biggest_score) + " >= beta: " + str(beta))
                    return biggest_score
                alpha = max(alpha, biggest_score)
                #if biggest_score > alpha:
                    #print(spaces + "Alpha: " + str(alpha))

        return biggest_score

class OpponentLearning(Agent):
    def __init__(self, evaluate_function,num_episodes,learning_rate,discount_factor):
        super().__init__()
        self.evaluate = evaluate_function
        self.episodes = num_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        
        self.Q = defaultdict(lambda: np.zeros(7))
        self.N = defaultdict(float)
        self.C = defaultdict(float)

        self.me = 0
        self.opponent = 1

    def decide(self, state):

        self.me = state.current_player.index
        self.opponent = self.me + 1 % 2

        p1_act = state.actions()
        act_vals = np.zeros(p1_act)
        for i, a1 in enumerate(p1_act):
            temp_next_state = state.act(a1)
            p2_act = state.actions()
            if temp_next_state is not None:
                for a2 in p2_act:
                    act_vals[i] += (self.C[state,a2]/self.N[state])*self.Q[state,a1,a2]

        a_m = p1_act[np.argmax(act_vals)]
        next_state = state.act(a_m)

        while True:
            if state.is_terminal:
                break 
            
            a_o = self.opponent.decide(next_state)
            r = state.reward(self.me) + self.evaluate(state, self.me)

            nextnext_state = next_state.act(a_o)
            p1_act = nextnext_state.actions()
            act_vals = np.zeros(p1_act)
            for i, a1 in enumerate(p1_act):
                temp_next_state = nextnext_state.act(a1)
                p2_act = nextnext_state.actions()
                if temp_next_state is not None:
                    for a2 in p2_act:
                        act_vals[i] += (self.C[nextnext_state,a2]/self.N[nextnext_state])*self.Q[nextnext_state,a1,a2]
            
            V_ns = max(act_vals)

            self.Q[state,a_m,a_o] = (1- self.learning_rate)*self.Q[state,a_m,a_o]+ self.learning_rate*(r+ self.discount_factor*V_ns)
            self.C[state,a_o] += 1
            self.N[state] += 1

            next_state = state
            




        a_o = 0 #change to get next move

        next_state = state.act(a_m)
        p1_act = next_state.actions()
        act_vals = np.zeros(p1_act)
        for i, a1 in enumerate(p1_act):
            temp_next_state = next_state.act(a1)
            p2_act = next_state.actions()
            if temp_next_state is not None:
                for a2 in p2_act:
                    act_vals[i] += (self.C[next_state,a2]/self.N[next_state])*self.Q[next_state,a1,a2]
        
        V_ns = p1_act[np.argmax(act_vals)]

        self.Q[state,a_m,a_o] = (1 - self.learning_rate)*self.Q[state,a_m,a_o] + self.learning_rate*(state.reward(self.me) + self.evaluate(next_state, self.me) + self.discount_factor*V_ns)
        self.C[state,a_o] += 1
        self.N[state] += 1






        

        print(state.players)
        

        return 0

   







