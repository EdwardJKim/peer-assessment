import sys
from peer_assessment.file import get_users
from peer_assessment.assign import make_anonymous

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    print(make_anonymous([i for i in range(20)]))

if __name__ == "__main__":
    main()

