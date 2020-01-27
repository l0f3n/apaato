# command_line_interface.py

import apaato.main as commands
import argparse


def load_wrapper(args):
    commands.load_accommodations()


def list_wrapper(args):
    commands.list_accommodations(show_link=args.link,
                                 show_type=args.type,
                                 show_location=args.location,)


def simulation_wrapper(args):
    combinations = commands.simulate(args.points,
                                     types=args.types,
                                     locations=args.locations, )
    commands.list_probabilites(combinations)


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands',
                                       description='Available commands',
                                       help='Which command to run',)

    # load
    load_parser = subparsers.add_parser("load")
    load_parser.set_defaults(func=load_wrapper)


    # list
    acc_parser = subparsers.add_parser("list")

    acc_parser.add_argument('--type',
                            help='(Default: False) Show the type of the accommodation',
                            action='store_true',)

    acc_parser.add_argument('--location',
                            help='(Default: False) Show the location that the accommodation is in',
                            action='store_true',)

    acc_parser.add_argument('-l', '--link',
                            help='(Default: False) Show link to accommodation',
                            action='store_true',)

    acc_parser.set_defaults(func=list_wrapper)


    # simulation
    sim_parser = subparsers.add_parser("simulate")

    sim_parser.add_argument('points',
                            type=int,
                            help='Queue points to simulate with',)

    sim_parser.add_argument('--types',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for accommodations of type \
                                  [Korridorrum|1 rum|2 rum|VALLAVÅNING| ... ]',)

    sim_parser.add_argument('--locations',
                            type=str,
                            nargs='+',
                            help='(Default: all) Only apply for accommodation at location \
                                  [Ryd|Flamman|Vallastaden|Irrblosset| ... ]',)

    sim_parser.set_defaults(func=simulation_wrapper, types=[], locations=[])

    clargs = parser.parse_args()

    clargs.func(clargs)
