# command_line_interface.py

import apaato.main as commands
import argparse


def load_wrapper(args):
    commands.load_accommodations()


def accommodations_wrapper(args):
    commands.list_accommodations(show_link=args.link,
                                 show_size=args.size,
                                 show_area=args.area,
                                 only_earliest_acceptance_date=args.only_earliest, )


def simulation_wrapper(args):
    combinations = commands.simulate(args.points,
                                     sizes=args.sizes,
                                     areas=args.areas,
                                     n=args.num,)
    commands.list_probabilites(combinations)


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands',
                                       description='Available commands',
                                       help='Which command to run',)

    # load
    load_parser = subparsers.add_parser("load")
    load_parser.set_defaults(func=load_wrapper)


    # accommodations
    acc_parser = subparsers.add_parser("accommodations")

    acc_parser.add_argument('-s', '--size',
                            help='(Default: False) Show the size of the accommodation',
                            action='store_true',)

    acc_parser.add_argument('-a', '--area',
                            help='(Default: False) Show the area that the accommodation is in',
                            action='store_true',)

    acc_parser.add_argument('-l', '--link',
                            help='(Default: False) Show link to accommodation',
                            action='store_true',)

    acc_parser.add_argument('--only-earliest',
                            help='(Default: False) Show only accommodations the ' +
                            'earliest latest application acceptance date',
                            action='store_true',)

    acc_parser.set_defaults(func=accommodations_wrapper)


    # simulation
    sim_parser = subparsers.add_parser("simulate")

    sim_parser.add_argument('points',
                            type=int,
                            help='Queue points to simulate with',)

    sim_parser.add_argument('--sizes',
                            type=str,
                            nargs='+',
                            help='(Default: all) What sizes of accommodations to apply for \
                                  [Korridorrum|1 rum|2 rum|VALLAVÅNING| ... ]',)

    sim_parser.add_argument('--areas',
                            type=str,
                            nargs='+',
                            help='(Default: all) What areas the accommodations needs to be in \
                                  [Ryd|Flamman|Vallastaden|Irrblosset| ... ]',)

    sim_parser.add_argument('--num',
                            type=int,
                            help='(Default: 1000) How many simulation to run per combination',)


    sim_parser.set_defaults(func=simulation_wrapper, sizes=[], areas=[], num=1000)

    clargs = parser.parse_args()

    clargs.func(clargs)
