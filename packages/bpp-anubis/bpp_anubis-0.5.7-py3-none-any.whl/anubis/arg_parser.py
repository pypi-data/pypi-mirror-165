import argparse


def parse_arguments():
    parser = argparse.ArgumentParser('Running in parallel mode')
    parser.add_argument('--processes', required=True, default=1, type=int)
    parser.add_argument('--feature_dir', required=True, default='features')
    parser.add_argument('--output', required=True, default='output')
    parser.add_argument('--aggregate', required=True, default='output/.tempres.json')
    parser.add_argument('--unit', required=False, default='scenario')
    parser.add_argument('--tags', required=False, nargs='*', action='append')
    parser.add_argument('-D', required=False, nargs='*', action='append')
    return parser.parse_known_args()
