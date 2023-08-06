import rich

from argparse import ArgumentParser
import os


def init_main():
    parser = ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    print(args.file)
    print(os.getcwd())


if __name__ == '__main__':
    init_main()


