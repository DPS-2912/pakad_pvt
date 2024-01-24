import argparse
from collector import collect

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--collect',
                        help='Add this flag to start capturing browsing traffic.',
                        default=False,
                        action='store_true')
    parser.add_argument('--open_world',
                        help='Add this flag for open_world scenario.',
                        default=False,
                        action='store_true')
    args = parser.parse_args()

    # Start traffic collector
    if args.collect:
        collect(args.open_world)