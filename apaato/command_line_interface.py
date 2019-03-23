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


def sim_wrapper(args):
    commands.simulate(args.points, filter_=args.filter)


def accommodations_wrapper(args):
    commands.list_accommodations(args.points, show_link=args.link)


def probabilities_wrapper(args):
    commands.list_probabilites()


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands',
                                       description='available commands',
                                       help='which command to run',)

    # load
    load_parser = subparsers.add_parser("load")
    load_parser.set_defaults(func=load_wrapper)


    # sim
    sim_parser = subparsers.add_parser("sim")
    sim_parser.add_argument('points',
                            type=int,
                            help='the amount of points to simulate with',)

    sim_parser.add_argument('-f', '--filter',
                             type=str,
                             help='what type of apartments to apply for',)

    sim_parser.set_defaults(func=sim_wrapper, filter='1 rum')


    # list #
    list_parser = subparsers.add_parser("list")
    list_subparser = list_parser.add_subparsers()

    # accommodations
    acc_parser = list_subparser.add_parser("accommodations")

    acc_parser.add_argument('points',
                            type=int,
                            help='the amount of points to sort by',)

    acc_parser.add_argument('-l', '--link',
                            help='if present, show link to accommodation',
                            action='store_true',)

    acc_parser.set_defaults(func=accommodations_wrapper)

    # probabilities
    prob_parser = list_subparser.add_parser("probabilites")
    prob_parser.set_defaults(func=probabilities_wrapper)

    clargs = parser.parse_args()

    clargs.func(clargs)
