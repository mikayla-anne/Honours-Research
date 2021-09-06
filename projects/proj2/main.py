#!/usr/bin/env python3

################################################################
## DO NOT MODIFY THIS FILE!
##
## If your agent and evaluation function are written correctly,
## then this file will work without issue.
##
## If you would like to run other tests, place it in a
## separate file and run it there.
################################################################

from ...lib import cli
from ...lib.game import Game, RandomAgent, discrete_soccer, connect_four
import sys
from . import agent, evaluation

game_module = {
    'discrete_soccer': discrete_soccer,
    'connect_four': connect_four
}
evaluations = {
    'discrete_soccer': evaluation.soccer,
    'connect_four': evaluation.connect_four
}

def run_game(args):
    agents = []

    if not args.game in game_module:
        sys.exit("Invalid game choice! Please choose from among: {}".format(game_module.keys()))

    gm = game_module[args.game]
    evaluation_fn = evaluations[args.game]

    minimax_agent = agent.MinimaxAgent(
        evaluation_fn,
        args.ab_pruning,
        args.max_depth
    )
    if args.interactive:
        interactive_agent = gm.InteractiveAgent()
        if cli.ask_yn("Will you play as the first player?"):
            agents = [interactive_agent, minimax_agent]
            if args.game == 'discrete_soccer':
                print("You will be playing on the RED team!")
            elif args.game == 'connect_four':
                print("You will be placing RED chips!")
        else:
            agents = [minimax_agent, interactive_agent]
            if args.game == 'discrete_soccer':
                print("You will be playing on the BLUE team!")
            elif args.game == 'connect_four':
                print("You will be placing BLACK chips!")
        print()
        if args.game == 'discrete_soccer':
            print("""Controls:
move: q w e
      a   d
      z x c

kick: space
""")
        elif args.game == 'connect_four':
            print("""Controls:
place chip: 1,2,3,4,5,6,7
""")
    else:
        agents = [minimax_agent, minimax_agent]

    game = Game(gm.generator(), agents)
    game.run(play_again='query', speed=2 if args.interactive else 0)


def main(cl_args):
    import argparse

    parser = argparse.ArgumentParser(description='Main function for Project 2: Minimax, Alpha-Beta Game Tree Search and Reinforcement Learning.')
    parser.add_argument('--max_depth', type=int, default=5, help='The maximum depth that minimax should search.')
    parser.add_argument('--ab_pruning', action='store_true', help='If included, use alpha-beta pruning.')
    parser.add_argument('--game', type=str, default='discrete_soccer', \
                        help='Game to play. (default: discrete_soccer)\n Options: discrete_soccer, connect_four')
    parser.add_argument('--interactive', action='store_true', default=False, \
                        help='If included, a human player will be able to join the game.')

    args = parser.parse_args(cl_args)

    run_game(args)


if __name__ == '__main__':
    main([])
