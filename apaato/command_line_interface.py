# command_line_interface.py

import apaato.main as commands
import argparse
import sys


def load_wrapper(args):
    commands.load_accommodations()


def list_wrapper(args):
    args_dict = vars(args)
    del args_dict['func']

    if args.all:
        for key in args_dict:
            args_dict[key] = True

    del args_dict['all']
        
    commands.list_accommodations(**args_dict)


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
    list_parser = subparsers.add_parser("list")

    list_parser.add_argument('--all',
                            help='(Default: False) Display all properties',
                            action='store_true',)

    list_parser.add_argument('--type',
                            help='(Default: False) Display type: [Korridorrum|1 rum|2 rum|VALLAVÅNING|...]',
                            action='store_true',)

    list_parser.add_argument('--location',
                            help='(Default: False) Display location: [Ryd|Irrblosset|Lambohov|...]',
                            action='store_true',)

    list_parser.add_argument('--queue',
                            help='(Default: False) Display queue',
                            action='store_true',)

    list_parser.add_argument('--rent',
                            help='(Default: False) Display rent',
                            action='store_true',)

    list_parser.add_argument('--elevator',
                            help='(Default: False) Display elevator status [Ja|Nej] (Yes|No)',
                            action='store_true',)

    list_parser.add_argument('--url',
                            help='(Default: False) Display url',
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
                            help='(Default: all) Only apply for type=[Korridorrum|1 rum|2 rum|VALLAVÅNING|...]',)

    prob_parser.add_argument('--location',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for location=[Ryd|Irrblosset|Lambohov|...]',)

    prob_parser.add_argument('--rent',
                            type=str,
                            help='(Default: all) Only apply for rent<=argument', )

    prob_parser.add_argument('--elevator',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for elevator=[Ja|Nej] (Yes|No)', )

    prob_parser.add_argument('--size',
                            type=str,
                            help='(Default: all) Only apply for size>=argument', )

    prob_parser.set_defaults(func=prob_wrapper)

    clargs = parser.parse_args()

    clargs.func(clargs)
