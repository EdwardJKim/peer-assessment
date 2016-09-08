import sys
from pgrader.assign import get_users, assign_notebooks
from pgrader.fetch import fetch_notebooks
from pgrader.autograde import get_peer_grading, get_peer_assessment
from pgrader.comments import get_comments


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        sys.stderr.write("Usage: pgrader <subcommand>\n")
        return 1

    users = get_users("studentlist.accy")

    if args[0] == "fetch":
        # fetch subcommand requires assignment_id
        if len(args[1:]) != 1:
            sys.stderr.write("Usage: pgrader fetch <assignment_id>\n")
            return 1
        assignment_id = args[1]
        for user in users:
            fetch_notebooks(
                "/home/ubuntu/export/exchange",
                "/home/ubuntu/submitted",
                user, "accy", assignment_id
            )

    elif args[0] == "assign":
        # assign subcommand requires assignment_id and week_number
        if len(args[1:]) != 2:
            sys.stderr.write("Usage: pgrader assign <assignment_id> <week_number>\n")
            return 1
        assignment_id = args[1]
        week_number = args[2]
        assign_notebooks(users, assignment_id, week_number, remove_header=True)

    elif args[0] == "given":
        # autograde subcommand requires assignment_id
        if len(args[1:]) != 1:
            sys.stderr.write("Usage: pgrader given <assignment_id>\n")
            return 1
        assignment_id = args[1]
        get_peer_grading(users, assignment_id)

    elif args[0] == "received":
        # autograde subcommand requires assignment_id and week_number
        if len(args[1:]) != 2:
            sys.stderr.write("Usage: pgrader received <assignment_id> <week_number>\n")
            return 1
        assignment_id = args[1]
        week_number = args[2]
        get_peer_assessment(users, assignment_id, week_number)

    elif args[0] == "comments":
        # autograde subcommand requires assignment_id and week_number
        if len(args[1:]) != 2:
            sys.stderr.write("Usage: pgrader comments <assignment_id> <week_number>\n")
            return 1
        assignment_id = args[1]
        week_number = args[2]
        get_comments(users, assignment_id, week_number)

    else:
        sys.stderr.write("Valid subcommands are: fetch, assign, given, received\n")


if __name__ == "__main__":
    main()

