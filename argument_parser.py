import argparse

def argument_parser():
    parser = argparse.ArgumentParser(description='Neural Match Academy Project')

    parser.add_argument('--top-choice', action='store_true', help='Top 10 Choice Regions')
    parser.add_argument('--save', action='store_true', help='Save or Plot')
    parser.add_argument('--n-bins', type=int, default=50, help='Number of Bins')
    parser.add_argument('--n-trials', type=int, default=10, help='Number of Trials to Plot')
    parser.add_argument('--sigma', type=int, default=3, help='Gaussian 1d filter sigma parameter')
    parser.add_argument('--wheel-to-mm', type=float, default=0.135, help='Wheel to mm parameter')

    args = parser.parse_args()
    return args