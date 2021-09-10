#!/usr/bin/env python3

import math, random


from ...lib.game import discrete_soccer, connect_four, GameState


def soccer(state: GameState, player_id):
    # TODO: Implement this function!
    score = 0
    player1 = state.players[player_id]
    #print("player1.x: " + str(player1.x))
    #print("player1.y: " + str(player1.y))
    #print("ball.x: " + str(state.ball.x))
    #print("ball.x: " + str(state.ball.x))

    #print("Distance to ball: " + str(p1_distance_to_ball))
    #score = 1
    # If player has the ball, he wants to be further toward their goal than them
    # If player doesn't have the ball,

    if player1.has_ball:
        #print("This player (P1) has the ball")
        score += 5

    for index, player2 in enumerate(state.players):
        #print("index: " + str(index))
        if index != player_id:
            if player1.has_ball:
                score += triangle_score(state, player1, player2, player1.team)
                #print("P1: " + str(player1.x) + ", " + str(player1.y))
                #print("P2: " + str(player2.x) + ", " + str(player2.y))
                #print("P1 triangle score (good): " + str(triangle_score(state, player1, player2, player2.team)))
            elif player2.has_ball:
                score -= triangle_score(state, player2, player1, player2.team)
                #print("P2 triangle score (bad): " + str(triangle_score(state, player2, player1, player1.team)))
            else:
                score += difference_to_ball(state, player1, player2)
                #print("P1: " + str(player1.x) + ", " + str(player1.y))
                #print("P2: " + str(player2.x) + ", " + str(player2.y))
                #print("Ball: " + str(state.ball.x) + ", " + str(state.ball.y))
                #print("How much closer P1 is to the ball vs P2: " + str(difference_to_ball(state, player1, player2)))
    """
        if index != player_id:
            p1_distance_to_p1_goal = abs(player1.x - state.goal_pos(player1.team)[0])
            p2_distance_to_p1_goal = abs(player2.x - state.goal_pos(player1.team)[0])
            if player2.has_ball:
                score -= 1
                if p1_distance_to_p1_goal >= p2_distance_to_p1_goal:
                    score -= 3
            else:
                if not player1.has_ball:
                    p1_distance_to_ball = math.sqrt(
                        pow(player1.x - state.ball.x, 2) + pow(player1.y - state.ball.y, 2))
                    p2_distance_to_ball = math.sqrt(
                        pow(player2.x - state.ball.x, 2) + pow(player2.y - state.ball.y, 2))
                    score += (p1_distance_to_p1_goal - p2_distance_to_p1_goal) / 10
    """
    # The soccer evaluation function *must* look into the game state
    # when running. It will then return a number, where the larger the
    # number, the better the expected reward (or lower bound reward)
    # will be.
    #
    # For a good evaluation function, you will need to
    # SoccerState-specific information. The file
    # `src/lib/game/discrete_soccer.py` provides a description of all
    # useful SoccerState properties.
    if not isinstance(state, discrete_soccer.SoccerState):
        raise ValueError("Evaluation function incompatible with game type.")
    #print("score: " + str(score))
    return score

def closerness_to_goal(state, player1, player2, goal_team):

    p1_dist = state.dist_to_goal((player1.x, player1.y), goal_team)
    p2_dist = state.dist_to_goal((player2.x, player2.y), goal_team)
    #print("p1 distance to goal: " + str(p1_dist))
    #print("p2 distance to goal: " + str(p2_dist))
    return p2_dist - p1_dist

def triangle_score(state, player1, player2, goal_team):
    goal_to_p2 = state.dist_to_goal((player2.x, player2.y), goal_team)
    #print("Goal -> P2: " + str(goal_to_p2))
    dist_between = distance_between_players(player1, player2)
    #print("P1 -> P2: " + str(dist_between))
    goal_to_p1 = state.dist_to_goal((player1.x, player1.y), goal_team)
    #print("Goal -> P1: " + str(goal_to_p1))
    return (goal_to_p2 + dist_between) - goal_to_p1

def difference_to_ball(state, player1, player2):
    p1_dist = math.sqrt(
        pow(player1.x - state.ball.x, 2) + pow(player1.y - state.ball.y, 2))
    p2_dist = math.sqrt(
        pow(player2.x - state.ball.x, 2) + pow(player2.y - state.ball.y, 2))
    return p2_dist - p1_dist

def distance_between_players(player1, player2):
    return math.sqrt(
        pow(player1.x - player2.x, 2) + pow(player1.y - player2.y, 2))

def connect_four(state, player_id):
    if not isinstance(state, connect_four.Connect4State):
        raise ValueError("Evaluation function incompatible with game type.")
    return 0
