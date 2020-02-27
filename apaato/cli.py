# command_line_interface.py

import apaato.main as commands
import argparse
import sys
from apaato import __version__

def load_wrapper(args):
    commands.load_accommodations()


def list_wrapper(args):
    display = {name: True for name in args.display}

    del args.func
    del args.display
    filter_ = vars(args)

    commands.list_accommodations(display, filter_)


def prob_wrapper(args):
    del args.func

    filter_ = vars(args)

    combinations = commands.simulate(filter_.pop('points'), filter_)
    commands.list_probabilites(combinations)


def main():

    parser = argparse.ArgumentParser(allow_abbrev=False, prog=__package__)

    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers()

    # load
    load_parser = subparsers.add_parser(
        'load',
        description='loads all accommodations into a database.',
        help='loads all accommodations into a database.',
    )

    load_parser.set_defaults(func=load_wrapper)

    # list
    list_parser = subparsers.add_parser(
        'list', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='lists all accommodations.',
        help='lists all accommodations.',
    )

    list_parser.add_argument(
        '--display',
        action='extend',
        nargs='+',
        default=['address', 'location', 'type'],
        choices=['elevator', 'floor', 'queue', 'rent', 'size', 'url'],
        help='Which properties to display',
        dest='display',
    )

    list_filter_group = list_parser.add_argument_group(
        'filters', 
        description='None (the default value) means that all values are allowed.'
    )

    list_filter_group.add_argument(
        '--type',
        type=str,
        nargs='+',
        help='Only list accommodations that has type',
        choices=['Korridorrum', '1 rum', '2 rum', '3 rum', 'VALLAVÅNING'],
    )

    list_filter_group.add_argument(
        '--location',
        type=str,
        nargs='+',
        help='Only list accommodations that located at',
        choices=['Fjärilen', 'Irrblosset', 'Lambohov', 'Ryd', 'Vallastaden'],
    )

    list_filter_group.add_argument(
        '--rent',
        type=str,
        help='Only list accommodations with rent less than', 
    )

    list_filter_group.add_argument(
        '--elevator',
        type=str,
        nargs='+',
        help='Only list accommodations with elevator', 
        choices=['Ja', 'Nej'],
    )

    list_filter_group.add_argument(
        '--size',
        type=str,
        help='Only list accommodations with size larger than', 
    )
    
    list_filter_group.add_argument(
        '--floor',
        type=str,
        nargs='+',
        help='Only list accommodations on floor', 
        choices=['1', '2', '3', '4', '5', '6'],
    )

    list_parser.set_defaults(func=list_wrapper)

    # prob
    prob_parser = subparsers.add_parser(
        'prob',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='lists the probabilities of getting the accommodation.',
        help='lists the probabilities of getting the accommodation.',
    )
    
    prob_parser.add_argument(
        'points',
        type=int,
        help='Queue points to simulate with',
    )

    prob_filter_group = prob_parser.add_argument_group(
        'filters', 
        description='None (the default value) means that all values are allowed',
    )

    prob_filter_group.add_argument(
        '--type',
        type=str,
        nargs='+',
        help='Apply for accommodations with type',
        choices=['Korridorrum', '1 rum', '2 rum', '3 rum', 'VALLAVÅNING'],
    )

    prob_filter_group.add_argument(
        '--location',
        type=str,
        nargs='+',
        help='Apply for accommodations at location',
        choices=['Fjärilen', 'Irrblosset', 'Lambohov', 'Ryd', 'Vallastaden'],
    )

    prob_filter_group.add_argument(
        '--rent',
        type=str,
        help='Apply for accommodations with rent less than', 
    )

    prob_filter_group.add_argument(
        '--elevator',
        type=str,
        nargs='+',
        help='Apply for accommodations with elevator', 
        choices=['Ja', 'Nej'],
    )

    prob_filter_group.add_argument(
        '--size',
        type=str,
        help='Apply for accommodations with size less than', 
    )
    
    prob_filter_group.add_argument(
        '--floor',
        type=str,
        nargs='+',
        help='Apply for acommodations on floor', 
        choices=['1', '2', '3', '4', '5', '6'],
    )

    prob_parser.set_defaults(func=prob_wrapper)

    # Begin parsing arguments

    # Display help and quit if no arguments were supplied
    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
        sys.exit(-1)
        
    args = parser.parse_args()

    args.func(args)
