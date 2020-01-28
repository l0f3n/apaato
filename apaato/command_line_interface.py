# command_line_interface.py

import apaato.main as commands
import argparse
import sys


def load_wrapper(args):
    commands.load_accommodations()


def list_wrapper(args):
    args_dict = vars(args)
    del args_dict['func']
    commands.list_accommodations(**args_dict)


def prob_wrapper(args):
    args_dict = vars(args)
    del args_dict['func']
    combinations = commands.simulate(args_dict.pop('points'), **args_dict)
    commands.list_probabilites(combinations)


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # load
    load_parser = subparsers.add_parser("load")
    load_parser.set_defaults(func=load_wrapper)

    # list
    list_parser = subparsers.add_parser("list")

    list_parser.add_argument('--type',
                            help='(Default: False) Show the type of the accommodation',
                            action='store_true',)

    list_parser.add_argument('--location',
                            help='(Default: False) Show the location that the accommodation is in',
                            action='store_true',)

    list_parser.add_argument('--url',
                            help='(Default: False) Show link to accommodation',
                            action='store_true',)

    list_parser.set_defaults(func=list_wrapper)

    # prob
    prob_parser = subparsers.add_parser("prob")

    prob_parser.add_argument('points',
                            type=int,
                            help='Queue points to simulate with',)

    prob_parser.add_argument('--type',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for accommodations of type \
                                  [Korridorrum|1 rum|2 rum|VALLAVÅNING| ... ]',)

    prob_parser.add_argument('--location',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for accommodation at location \
                                  [Ryd|Flamman|Vallastaden|Irrblosset| ... ]',)

    prob_parser.add_argument('--hiss',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for accommodation with elevator (Ja) or without (Nej) \
                                  [Ja|Nej]',)


    prob_parser.set_defaults(func=prob_wrapper, type=[], location=[], hiss=[])

    clargs = parser.parse_args()

    # Quit if no arguments were supplied
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(-1)

    clargs.func(clargs)
