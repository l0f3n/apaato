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
    list_parser = subparsers.add_parser("list", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    list_parser.add_argument('--all',
                            help='Display all properties',
                            action='store_true',)

    list_parser.add_argument('--type',
                            help='Display type: [Korridorrum|1 rum|2 rum|VALLAVÅNING|...]',
                            action='store_true',)

    list_parser.add_argument('--location',
                            help='Display location: [Ryd|Irrblosset|Lambohov|...]',
                            action='store_true',)

    list_parser.add_argument('--queue',
                            help='Display queue',
                            action='store_true',)

    list_parser.add_argument('--rent',
                            help='Display rent',
                            action='store_true',)

    list_parser.add_argument('--elevator',
                            help='Display elevator status [Ja|Nej] (Yes|No)',
                            action='store_true',)
    
    list_parser.add_argument('--size',
                        help='Display size',
                        action='store_true',)
    
    list_parser.add_argument('--floor',
                        help='Display floor',
                        action='store_true',)

    list_parser.add_argument('--url',
                            help='Display url',
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

    clargs = parser.parse_args()
    
    clargs.func(clargs)
