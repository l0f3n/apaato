# command_line_interface.py

import apaato.main as commands
import argparse


def load_wrapper(args):
    commands.load_accommodations()


def accommodations_wrapper(args):
    commands.list_accommodations(queue_points=args.points,
                                 show_link=args.link,
                                 only_earliest_acceptance_date=args.only_earliest, )


def simulation_wrapper(args):
    combinations = commands.simulate(args.points,
                                     size=args.sizes,
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

    acc_parser.add_argument('-p', '--points',
                            type=int,
                            help='If present, sort apartments by position in queue',)

    acc_parser.add_argument('-l', '--link',
                            help='(Default: False) Show link to accommodation',
                            action='store_true',)

    acc_parser.add_argument('--only-earliest',
                            help='(Default: False) Show only accommodations the ' +
                            'earliest latest application acceptance date',
                            action='store_true',)

    acc_parser.set_defaults(func=accommodations_wrapper, points=0)


    # simulation
    sim_parser = subparsers.add_parser("simulate")

    sim_parser.add_argument('points',
                            type=int,
                            help='Queue points to simulate with',)

    sim_parser.add_argument('-s', '--sizes',
                            type=str,
                            nargs='+',
                            help='(Default: all) What sizes of accommodations to apply for \
                            [Korridorrum|1 rum|2 rum|VALLAVÅNING| ... ]',)

    sim_parser.add_argument('-n', '--num',
                            type=int,
                            help='(Default: 1000) How many simulation to run per combination',)


    sim_parser.set_defaults(func=simulation_wrapper, sizes=[], num=1000)

    clargs = parser.parse_args()

    clargs.func(clargs)
