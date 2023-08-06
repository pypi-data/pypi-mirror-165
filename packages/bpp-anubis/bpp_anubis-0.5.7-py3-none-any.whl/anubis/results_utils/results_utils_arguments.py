import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', '-f', required=True, default=[], nargs='+')
    parser.add_argument('--output_file', '-o', required=True)
    return parser.parse_args()
