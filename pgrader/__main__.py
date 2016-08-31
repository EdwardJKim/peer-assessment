import sys
from pgrader.assign import get_users, assign_notebooks
from pgrader.fetch import fetch_notebooks


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        sys.stderr.write("Usage: pgrader <subcommand>\n")
        return 1

    users = get_users("studentlist.accy")

    if args[0] == "fetch":
        for user in users:
            fetch_notebooks(
                "/home/ubuntu/export/exchange",
                "/home/ubuntu/submitted",
                user, "accy", "accy570_hw1_due_8_30"
            )
    elif args[0] == "assign":
        assign_notebooks(users, "week1", 1, remove_header=True)
    else:
        sys.stderr.write("Valid subcommands are: fetch, assign\n")


if __name__ == "__main__":
    main()

