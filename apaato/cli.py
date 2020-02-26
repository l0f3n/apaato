# command_line_interface.py

import apaato.main as commands
import argparse
import sys


def load_wrapper(args):
    commands.load_accommodations()


def list_wrapper(args):
    display = {name: True for name in args.display}
    commands.list_accommodations(display)


def prob_wrapper(args):
    args_dict = vars(args)
    del args_dict['func']
    combinations = commands.simulate(args_dict.pop('points'), **args_dict)
    commands.list_probabilites(combinations)


def main():

    parser = argparse.ArgumentParser()

    # Quit if no arguments were supplied
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(-1)

    subparsers = parser.add_subparsers()

    # load
    load_parser = subparsers.add_parser("load")
    load_parser.set_defaults(func=load_wrapper)

    # list
    list_parser = subparsers.add_parser("list", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    list_parser.add_argument('--display',
        action='extend',
        nargs='+',
        default=['address', 'location', 'type'],
        choices=['elevator', 'floor', 'queue', 'rent', 'size', 'url'],
        help='Which properties to display',
        dest='display',
        )

    list_parser.set_defaults(func=list_wrapper)

    # prob
    prob_parser = subparsers.add_parser("prob")

    prob_parser.add_argument('points',
                            type=int,
                            help='Queue points to simulate with',)

    prob_parser.add_argument('--type',
                            type=str,
                            nargs='+',
                            help='Apply for accommodations with type',
                            choices=['Korridorrum', '1 rum', '2 rum', '3 rum', 'VALLAVÅNING'],
                            )

    prob_parser.add_argument('--location',
                            type=str,
                            nargs='+',
                            help='Apply for accommodations at location',
                            choices=['Fjärilen', 'Irrblosset', 'Lambohov', 'Ryd', 'Vallastaden'],
                            )

    prob_parser.add_argument('--rent',
                            type=str,
                            help='Apply for accommodations with rent less than', )

    prob_parser.add_argument('--elevator',
                            type=str,
                            nargs='+',
                            help='Apply for accommodations with elevator', 
                            choices=['Ja', 'Nej'],
                            )

    prob_parser.add_argument('--size',
                            type=str,
                            help='Apply for accommodations with size less than', )
    
    prob_parser.add_argument('--floor',
                            type=str,
                            nargs='+',
                            help='Apply for acommodations on floor', 
                            choices=['1', '2', '3', '4', '5', '6'],
                            )

    prob_parser.set_defaults(func=prob_wrapper)

    args = parser.parse_args()

    args.func(args)
