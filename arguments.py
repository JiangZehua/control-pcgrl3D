from pdb import set_trace as T
import argparse

prob_cond_metrics = {
        'binary_ctrl': ['regions', 'path-length'],
        'zelda_ctrl': ['nearest-enemy', 'path-length'],
        'sokoban_ctrl': ['crate', 'sol-length'],
        }

all_metrics = {
        'binarygoal': ['regions', 'path-length'],
        'zeldagoal': ['player', 'key', 'door', 'enemies', 'regions', 'nearest-enemy', 'path-length'],
        'sokobangoal': ['player', 'crate', 'sol-length'],
        }

def parse_args():
    args = get_args()
    return parse_pcgrl_args(args)


def parse_pcgrl_args(args):
    opts = args.parse_args()
    if opts.max_step == -1:
        max_step = None
    if opts.conditionals == ['NONE']:
        opts.conditionals = []
    elif opts.conditionals == ['DEFAULT']:
        opts.conditionals = prob_cond_metrics[opts.problem]
    elif opts.conditionals == ['ALL']:
        opts.conditionals = all_metrics[opts.problem]

    return opts

def get_args():
    args = argparse.ArgumentParser(description='Conditional PCGRL')
    args.add_argument(
        '-p',
        '--problem',
        help='which problem (i.e. game) to generate levels for (binary, sokoban, zelda, mario, ... roller coaster tycoon, simcity???)',
        default='binary_ctrl')
    args.add_argument(
        '-r',
        '--representation',
        help='Which representation to use (narrow, turtle, wide, ... cellular-automaton???)',
        default='narrow')
    args.add_argument(
        '-ca',
        '--ca_action',
        help='Cellular automaton-type action. The entire next game state is sampled from the model output.',
        action='store_true',
    )
    args.add_argument(
        '-c',
        '--conditionals',
        nargs='+',
        help='Which game level metrics to use as conditionals for the generator',
        default=['DEFAULT'])
    args.add_argument(
        '--resume',
        help='Are we resuming from a saved training run?',
        action="store_true",)
    args.add_argument(
        '--experiment_id',
        help='An experiment ID for tracking different runs of experiments with identical hyperparameters.',
        default=None)
    args.add_argument(
        '--midep_trgs',
        help='Do we sample new (random) targets mid-episode, or nah?',
        action='store_true',)
    args.add_argument(
        '--n_cpu',
        help='How many environments to run in parallel.',
        type=int,
        default=50,
    )
    args.add_argument(
        '--render',
        help='Render an environment?',
        action='store_true',
    )
    args.add_argument(
        '--load_best',
        help='Whether to load the best saved model of a given run rather than the latest.',
        action='store_true',)
    args.add_argument(
        '--crop_size',
        help='Hackishly control crop size of agent observation.',
        type=int,
        default=-1,
        )
    args.add_argument(
        '--max_step',
        help='How many steps in an episode, maximum.',
        type=int,
        default=-1,
        )
    args.add_argument(
        '--alp_gmm',
        help='Fancy ish teacher algorithm for controllable targets.',
        action='store_true',
    )

    # Not for training:
    args.add_argument(
        '--HPC',
        help='Load from "hpc_runs" (rather than "runs") directory.',
        action='store_true',
        )

    return args