import sys
from pgrader.file import get_users
from pgrader.assign import make_table

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    print(make_table([str(i) for i in range(20)], 10))

if __name__ == "__main__":
    main()

