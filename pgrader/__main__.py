import sys
from pgrader.assign import get_users, assign_notebooks


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    users = get_users("studentlist.accy")
    assign_notebooks(users, "test", 0)


if __name__ == "__main__":
    main()

