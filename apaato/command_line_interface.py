# command_line_interface.py

#               command_line_interface.py
#                          |
#                        main.py
#                          |
#     +------------+-------+---------+----------------+
#     |            |                 |                |
# scraper.py   database.py   text_formatter.py   simulation.py
#     |            |                 |                |
#     +------------+-------+---------+----------------+
#                          |
#                     accommodation.py


import apaato.main as commands
import argparse


def load_wrapper(args):
    commands.load_accommodations()


def accommodations_wrapper(args):
    commands.list_accommodations(args.points, show_link=args.link)


def simulation_wrapper(args):
    combinations = commands.simulate(args.points, filter_=args.filter)
    commands.list_probabilites(combinations)


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands',
                                       description='available commands',
                                       help='which command to run',)

    # load
    load_parser = subparsers.add_parser("load")
    load_parser.set_defaults(func=load_wrapper)


    # accommodations
    acc_parser = subparsers.add_parser("accommodations")

    acc_parser.add_argument('points',
                            type=int,
                            help='the amount of points to sort by',)

    acc_parser.add_argument('-l', '--link',
                            help='if present, show link to accommodation',
                            action='store_true',)

    acc_parser.set_defaults(func=accommodations_wrapper)


    # simulation
    sim_parser = subparsers.add_parser("simulate")

    sim_parser.add_argument('points',
                            type=int,
                            help='the amount of points to simulate with',)

    sim_parser.add_argument('-s', '--size',
                            type=str,
                            help="what size of accommodation to apply for. \
                            (eg. 'Korridorrum', '1 rum' etc.)",)

    sim_parser.set_defaults(func=simulation_wrapper, filter='1 rum')

    clargs = parser.parse_args()

    clargs.func(clargs)
