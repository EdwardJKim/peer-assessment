import sys
from peer_assessment.names_generator import get_random_name


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    print(get_random_name())


if __name__ == "__main__":
    main()

